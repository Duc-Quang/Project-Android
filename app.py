from flask import Flask, request
from flask_restful import Api
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin 

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myclient = pymongo.MongoClient("mongodb+srv://quang123:quang123@appshop.fk9pu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient['android']
mycol = mydb['user']

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/signup/<username>/<email>/<password>')
@cross_origin()
def save_data_user(username, email, password):

    x = mycol.find_one({"username": str(username)})
    if x != None:
        return {
            'status': 'Error'
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
            'status': 'success',
        }
    return {
        'Error': 'Not found user'
    }

@app.route('/signups')
@cross_origin()
def save_data():
    api_key = request.values.get('api_key')
    username = request.values.get('username')
    email = request.values.get('email')
    password = request.values.get('password')

    if api_key == '46ec83c05e17370e71c1ad416e76efd1':
        x = mycol.find_one({"username": str(username)})
        if x != None:
            return {
                'status': 'Error'
            }
        mycol.insert_one({"_id": ObjectId(),"username": str(username), "email": str(email), "password": str(password)})
        return {
            'Status': 'success',
        }

@app.route('/signins')
@cross_origin()
def check_data():
    api_key = request.values.get('api_key')
    username = request.values.get('username')
    password = request.values.get('password')

    if api_key == '46ec83c05e17370e71c1ad416e76efd1':
        x = mycol.find_one({"username": str(username)})
        if x['password'] == password:
            return {
                'status': 'success',
            }
        return {
            'Error': 'Not found user'
        }

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)