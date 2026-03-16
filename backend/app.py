# app.py
from flask import Flask, request, jsonify
import redis
import socket
import os

app = Flask(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis-service')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)


# Redis Verbindung
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

@app.route('/')
def hello():
    return jsonify(message="Hello, World!", host=socket.gethostname())

@app.route('/api')
def api():
    return jsonify(message="This is the API response", host=socket.gethostname())

@app.route("/api/kv", methods=["POST"])
def store_kv():
    data = request.get_json()

    key = data.get("key")
    value = data.get("value")

    if not key or value is None:
        return jsonify({"error": "key and value required"}), 400

    r.set(key, value)

    return jsonify({
        "status": "stored",
        "key": key,
        "value": value
    })


@app.route("/api/kv", methods=["GET"])
def get_kv():
    key = request.args.get("key")

    # einzelner key
    if key:
        value = r.get(key)
        return jsonify({key: value})

    # alle keys
    keys = r.keys("*")
    result = {}

    for k in keys:
        result[k] = r.get(k)

    return jsonify(result)

@app.route("/api/kv", methods=["DELETE"])
def delete_kv():
    key = request.args.get("key")

    if not key:
        return jsonify({"error": "key required"}), 400

    removed = r.delete(key)

    if removed == 0:
        return jsonify({"status": "not found", "key": key})

    return jsonify({"status": "deleted", "key": key})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
