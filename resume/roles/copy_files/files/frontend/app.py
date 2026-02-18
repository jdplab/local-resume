import os
from flask import Flask, render_template, request, send_from_directory, Response, session, make_response
from redis import Redis, ConnectionPool
from gevent import monkey
import json
import atexit
import time
import logging
import uuid

monkey.patch_all()

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("SECRET_KEY")
app.config['REDIS_URL'] = os.getenv("REDIS_URL")

pool = ConnectionPool.from_url(app.config['REDIS_URL'])
redis_client = Redis(connection_pool=pool)

def get_visitor_count():
    return int(redis_client.get('visitor_count') or 0)

def get_unique_visitors_count():
    return redis_client.hlen('user_visits')

@app.route("/")
def index():
    try:
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
            ip_address = "home"
        
        visitor_id = request.cookies.get('visitor_id')
        logging.debug(f"Visitor ID from cookie: {visitor_id}")
        
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            redis_client.incr('visitor_count')
            redis_client.hincrby('user_visits', visitor_id, 1)
            logging.debug(f"New visitor ID generated and Redis updated: {visitor_id}")
        else:
            logging.debug(f"Existing visitor ID: {visitor_id}")
        
        session["ip_address"] = ip_address
        stats = {"visitor_count": get_visitor_count(), "unique_visitors": get_unique_visitors_count()}
        
        response = make_response(render_template('index.html', stats=stats))
        response.set_cookie('visitor_id', visitor_id, max_age=60*60*24*30, path='/', httponly=True, samesite='Lax')
        logging.debug(f"Set cookie with visitor ID: {visitor_id}")
        return response
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        raise

@app.route("/JonathanPolanskyResume.pdf")
def static_from_root():
    try:
        return send_from_directory(app.static_folder, request.path[1:])
    except Exception as e:
        logging.error(f"Error downloading resume: {e}")
        raise

@app.route('/stream')
def stream():
    try:
        ip_address = session.get("ip_address")
        def event_stream(ip_address):
            while True:
                try:
                    data = {
                        "visitor_count": get_visitor_count(),
                        "unique_visitors": get_unique_visitors_count()
                    }
                    yield f'data: {json.dumps(data)}\n\n'
                    time.sleep(1) 
                except GeneratorExit:
                    break
        
        return Response(event_stream(ip_address), mimetype='text/event-stream')
    except Exception as e:
        logging.error(f"Error in stream route: {e}")
        raise

def cleanup():
    redis_client.close()

atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
