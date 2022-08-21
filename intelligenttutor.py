from concurrent.futures import thread
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    response = dict({'app': 'intelligenttutor'})
    return jsonify(response)

@app.route('/intelligenttutor/api', methods = ['POST'], endpoint = 'api')
def kinematic():
    req = req.get_json()
    print(req)
    return jsonify(dict({'response': 'true'}))

if __name__ == '__main__':
    app.run(threaded = True, port = 5000)