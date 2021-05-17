from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_restful import Api
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin 

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['android']
mycol = mydb['user']

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/signup/<username>/<email>/<password>')
@cross_origin()
def save_data_user(username, email, password):
    x = mycol.find_one({"username": str(username)})
    if x["username"] == username:
        return {
            'Status': 'Error'
        }
    mycol.insert_one({"_id": ObjectId(),"username": str(username), "email": str(email), "password": str(password)})
    return {
        'Status': 'success',
    }
@app.route('/signin/<username>/<password>')
@cross_origin()
def check_data_user(username, password):
    x = mycol.find_one({"username": str(username)})
    if x['password'] == password:
        return {
            'Status': 'success',
        }
    return {
        'Error': 'Not found user'
    }

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)