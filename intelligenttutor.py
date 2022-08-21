from concurrent.futures import thread
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from sympy import *
import math

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

def positiveRad(angle):
    if angle < 0:
        angle = 2*math.pi + angle
    return angle

@app.route('/')
def index():
    response = dictionary()
    response.add('app', 'intelligenttutor-api')
    return jsonify(response)

@app.route('/intelligenttutor/api', methods = ['POST'], endpoint = 'api')
@cross_origin()
def kinematic():
    r = []
    th = []

    req = request.get_json()
    res = dictionary()

    for data in req['r']:
        r.append(data['magnitude'])
    res.add('r', stringifyArray(r))

    for data in req['theta']:
        th.append(data['magnitude'])

    # Declare symbolic variables
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)

    # Solve for angular position
    f1 = r[2]*cos(x) - r[3]*cos(y) - r[0] + r[1]*cos(th[1])
    f2 = r[2]*sin(x) - r[3]*sin(y) + r[1]*sin(th[1])
    sol = solve([f1, f2], x, y)
    if sol[0][0] > 0:
        th.append(positiveRad(sol[0][0]))
        th.append(positiveRad(sol[0][1]))
    else:
        th.append(positiveRad(sol[1][0]))
        th.append(positiveRad(sol[1][1]))
    res.add('theta', stringifyArray(th))

    return jsonify(res), 200

if __name__ == '__main__':
    app.run(debug = True, threaded = True, port = 5000)