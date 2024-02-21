from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_sse import sse
from redis import Redis, ConnectionPool
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logging.debug('logging is working')

app = Flask(__name__, static_folder="static")
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.register_blueprint(sse, url_prefix='/stream')

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
    
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
        ip_address = "home"
  
    count = get_visitor_count()
    uniquevisitors = get_unique_visitors_count()
    visits = get_user_visits(ip_address)
    return render_template("index.html", visitor_count=count, unique_visitors=uniquevisitors, user_visits=visits)

@app.route("/JonathanPolanskyResume.docx")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/update-stats')
def update_stats():

    logging.debug('update_stats function called')

    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
        ip_address = "home"
  
    redis_client.incr('visitor_count')
    redis_client.hincrby('user_visits', ip_address, 1)
    stats = {"visitor_count": get_visitor_count(), "unique_visitors": get_unique_visitors_count(), "user_visits": get_user_visits(ip_address)}

    logging.debug('stats updated and put into stats array')

    stats_json = json.dumps(stats)

    redis_client.publish('stats_channel', stats_json)

    logging.debug('stats published to redis')

    return 'Stats updated and published to Redis'

@app.route('/stream')
def stream():
    logging.debug('Accessing /stream endpoint')  # Log statement to check if the /stream endpoint is accessed
    return sse.stream()

with app.app_context():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('stats_channel')

@app.teardown_appcontext
def teardown(exception):
    pubsub.unsubscribe('stats_channel')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
