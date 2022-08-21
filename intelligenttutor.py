from concurrent.futures import thread
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(dict({'app': 'intelligenttutor'}))

if __name__ == '__main__':
    app.run(threaded = True, port = 5000)