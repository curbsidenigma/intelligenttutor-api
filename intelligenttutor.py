from concurrent.futures import thread
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

class dictionary(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

def stringifyArray(array):
    stringified = []
    for element in array:
        stringified.append(str(round(element, 2)))
    return stringified

@app.route('/')
def index():
    response = dictionary()
    response.add('app', 'intelligenttutor-api')
    return jsonify(response)

@app.route('/intelligenttutor/api', methods = ['POST'], endpoint = 'api')
@cross_origin()
def kinematic():
    r = []

    req = request.get_json()
    res = dictionary()

    for data in req['r']:
        r.append(data['magnitude'])
    res.add('r', stringifyArray(r))

    return jsonify(res), 200

if __name__ == '__main__':
    app.run(debug = True, threaded = True, port = 5000)