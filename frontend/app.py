from flask import Flask, render_template, request, send_from_directory, Response, session, jsonify
from redis import Redis, ConnectionPool
from gevent import monkey
import json
import logging
import signal
import sys
import time

monkey.patch_all()

logging.basicConfig(level=logging.WARNING)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

app = Flask(__name__, static_folder="static")
app.secret_key = "secret_key"
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.logger.addHandler(file_handler)

# Initialize Redis connection pool and client
pool = ConnectionPool.from_url(app.config['REDIS_URL'])
redis_client = Redis(connection_pool=pool)

def signal_handler(sig, frame):
    logging.warning('Signal handler called')
    redis_client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_visitor_count():
    return int(redis_client.get('visitor_count') or 0)

def get_unique_visitors_count():
    return redis_client.hlen('user_visits')

@app.route("/")
def index():
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
        ip_address = "home"
    session["ip_address"] = ip_address
    redis_client.incr('visitor_count')
    redis_client.hincrby('user_visits', ip_address, 1)
    stats = {"visitor_count": get_visitor_count(), "unique_visitors": get_unique_visitors_count()}
    return render_template('index.html', stats=stats)

@app.route("/JonathanPolanskyResume.docx")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/stream')
def stream():
    ip_address = session.get("ip_address")
    
    def event_stream(ip_address):
        while True:
            try:
                data = {
                    "visitor_count": get_visitor_count(),
                    "unique_visitors": get_unique_visitors_count()
                }
                yield f'data: {json.dumps(data)}\n\n'
                time.sleep(1)  # delay for 1 second
            except GeneratorExit:
                logging.warning('GeneratorExit caught')
                break
    
    return Response(event_stream(ip_address), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
