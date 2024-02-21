from flask import Flask, render_template, request, send_from_directory, Response, session
from redis import Redis, ConnectionPool
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logging.debug('logging is working')
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

app = Flask(__name__, static_folder="static")
app.secret_key = "secret_key"
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.logger.addHandler(file_handler)

redis_pool = ConnectionPool.from_url(app.config['REDIS_URL'])
redis_client = Redis(connection_pool=redis_pool)

def get_visitor_count():
    return int(redis_client.get('visitor_count') or 0)

def get_user_visits(ip_address):
    return int(redis_client.hget('user_visits', ip_address) or 0)

def get_unique_visitors_count():
    return redis_client.hlen('user_visits')

@app.route("/")
def index():
    logging.debug('Index function called')
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
        ip_address = "home"
    session["ip_address"] = ip_address
    redis_client.incr('visitor_count')
    redis_client.hincrby('user_visits', ip_address, 1)
    stats = {"visitor_count": get_visitor_count(), "unique_visitors": get_unique_visitors_count(), "user_visits": get_user_visits(ip_address)}
    logging.debug('stats updated and put into stats array')
    stats_json = json.dumps(stats)
    redis_client.publish('stats_channel', stats_json)
    logging.debug('stats published to redis')
    return render_template('index.html')

@app.route("/JonathanPolanskyResume.docx")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/stream')
def stream():
    ip_address = session.get("ip_address")
    def event_stream(ip_address):
        initial_data = json.dumps({
            "visitor_count": get_visitor_count(),
            "unique_visitors": get_unique_visitors_count(),
            "user_visits": get_user_visits(ip_address)
        })
        yield f'data: {initial_data}\n\n'
        pubsub = redis_client.pubsub()
        pubsub.subscribe('stats_channel')
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode())
                if 'user_visits' in data:
                    data['user_visits'] = get_user_visits(ip_address)
                yield f'data: {json.dumps(data)}\n\n'
    return Response(event_stream(ip_address), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)