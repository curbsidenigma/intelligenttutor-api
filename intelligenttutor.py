from concurrent.futures import thread
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    response = dict({'app': 'intelligenttutor'})
    return jsonify(response)

@app.route('/intelligenttutor/api', methods = ['POST'], endpoint = 'api')
@cross_origin()
def kinematic():
    req = request.get_json()
    return jsonify(dict({'response': 'true'}))

if __name__ == '__main__':
    app.run(debug = True, threaded = True, port = 5000)