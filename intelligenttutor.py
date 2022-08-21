from concurrent.futures import thread
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return jsonify(dict({'app': 'intelligenttutor'}))

if __name__ == '__main__':
    app.run(threaded = True, port = 5000)