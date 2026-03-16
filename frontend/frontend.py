# frontend.py
from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

# Use environment variable for the backend URL
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://flask-api-service')

@app.route('/')
def home():
    response = requests.get(f"{BACKEND_URL}/api")
    return render_template_string("""
        <html>
            <body>
                <h1>Load Balancing Demo</h1>
                <p>Response from backend: {{ response.json() }}</p>
                <button onclick="window.location.reload();">Refresh</button>
            </body>
        </html>
    """, response=response)


HTML = """
<!doctype html>
<html>
<body>

<h2>Store Key Value</h2>
<form method="post" action="/kv/store">
  Key: <input name="key">
  Value: <input name="value">
  <button type="submit">Save</button>
</form>

<h2>Read Key Value</h2>
<form method="get" action="/kv/view">
  Key (optional): <input name="key">
  <button type="submit">Load</button>
</form>

{% if data %}
<h2>Result</h2>
<ul>
{% for k,v in data.items() %}
  <li><b>{{k}}</b> : {{v}}</li>
{% endfor %}
</ul>
{% endif %}

<h2>Delete Key</h2>
<form method="post" action="/kv/delete">
  Key: <input name="key">
  <button type="submit">Delete</button>
</form>

</body>
</html>
"""


@app.route("/kv")
def kv_index():
    return render_template_string(HTML)


@app.route("/kv/store", methods=["POST"])
def kv_store():
    key = request.form.get("key")
    value = request.form.get("value")

    requests.post(f"{BACKEND_URL}/api/kv", json={"key": key, "value": value})

    return "stored <br><a href='/kv'>back</a>"


@app.route("/kv/view")
def kv_view():
    key = request.args.get("key")

    if key:
        r = requests.get(f"{BACKEND_URL}/api/kv", params={"key": key})
    else:
        r = requests.get(f"{BACKEND_URL}/api/kv")

    data = r.json()

    return render_template_string(HTML, data=data)


@app.route("/kv/delete", methods=["POST"])
def kv_delete():
    key = request.form.get("key")

    requests.delete(f"{BACKEND_URL}/api/kv", params={"key": key})

    return f"deleted {key} <br><a href='/kv'>back</a>"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
