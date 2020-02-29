from flask import Flask, jsonify

import config

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/name/<value>')
def name(value):
    val = {"value": value}
    return jsonify(val)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)