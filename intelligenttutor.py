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
    response = dict({
        'name': 'intelligenttutor-api',
        'version': '3.0.2',
        'authors': [
            {
                'id': '1',
                'name': 'Gerardo Dominguez Ramirez'
            }
        ],
        'variables': [
            {
                'id': '1',
                'name': 'position',
                'symbol': 'r'
            },
            {
                'id': '2',
                'name': 'angular position',
                'symbol': 'theta'
            },
            {
                'id': '3',
                'name': 'angular velocity',
                'symbol': 'omega'
            },
            {
                'id': '4',
                'name': 'angular acceleration',
                'symbol': 'alpha'
            }
        ]
    })
    return jsonify(response)

@app.route('/intelligenttutor/api', methods = ['POST'], endpoint = 'api')
@cross_origin()
def kinematic():
    r = []
    th = []
    om = []
    al = []

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

    # Solve for angular velocity
    for data in req['omega']:
        om.append(data['magnitude'])
    f1 = -r[2]*sin(th[2])*x + r[3]*sin(th[3])*y - r[1]*om[1]*sin(th[1])
    f2 = r[2]*cos(th[2])*x - r[3]*cos(th[3])*y + r[1]*om[1]*cos(th[1])
    sol = solve([f1, f2], x, y)
    om.append(sol[x].subs({x:1}).evalf(16))
    om.append(sol[y].subs({x:1}).evalf(16))
    res.add('omega', stringifyArray(om))

    # Solve for angular acceleration
    for data in req['alpha']:
        al.append(data['magnitude'])
    f1 = -r[2]*sin(th[2])*x + r[3]*sin(th[3])*y - r[1]*al[1]*sin(th[1]) - r[1]*(om[1]**2)*cos(th[1]) - r[2]*(om[2]**2)*cos(th[2]) + r[3]*(om[3]**2)*cos(th[3])
    f2 = r[2]*cos(th[2])*x - r[3]*cos(th[3])*y + r[1]*al[1]*cos(th[1]) - r[1]*(om[1]**2)*sin(th[1]) - r[2]*(om[2]**2)*sin(th[2]) + r[3]*(om[3]**2)*sin(th[3])
    sol = solve([f1, f2], x, y)
    al.append(sol[x].subs({x:1}).evalf(16))
    al.append(sol[y].subs({y:1}).evalf(16))
    res.add('alpha', stringifyArray(al))

    return jsonify(res), 200

if __name__ == '__main__':
    app.run(debug = True, threaded = True, port = 5000)