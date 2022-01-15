from flask import Flask, request, render_template, send_from_directory, Response
from flask_restful import Api
import hashlib
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin 
import constants as Const
import os
import glob
import json
import datetime

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

myclient = pymongo.MongoClient(Const.PATH_MONGO)
mydb = myclient['android']
mycol_user = mydb['user']

@app.route('/')
def hello():
    return 'Hello world!'
    # return render_template('index.html')

# ===========SIGNIN/SIGNUP-POST===========
@app.route('/signup', methods=['POST'])
@cross_origin()
def save_data_user_post():
    username = request.json['username']
    idcard = request.json['idcard']
    address = request.json['address']
    carnum = request.json['carnum']
    # img license plates
    password = request.json['password']

    check_username = mycol_user.find_one({"username": str(username)})
    check_idcard = mycol_user.find_one({"idcard": str(idcard)})
    check_carnum = mycol_user.find_one({"carnum": str(carnum)})

    if check_username != None:
        return {
            'status': 'username has been exists'
        }
    if check_idcard != None:
        return {
            'status': 'idcard has been exists'
        }
    if check_carnum != None:
        return {
            'status': 'carnum has been exists'
        }
    
    result = hashlib.md5(password.encode())
    password = result.hexdigest()
    mycol_user.insert_one({"_id": ObjectId(),"username": str(username), "idcard": str(idcard), "carnum": str(carnum), "address": str(address), "password": str(password)})
    return {
        'status': 'success'
    }

@app.route('/signin', methods=['POST'])
@cross_origin()
def check_data_user_post():
    username = request.json['username']
    password = request.json['password']

    x = mycol_user.find_one({"username": username})
    result = hashlib.md5(password.encode())
    password = result.hexdigest()

    if x != None and x['password'] == str(password):
        _id = x['_id']
        idcard = x['idcard']
        return {
            'status': 'success',
            'id_user': f'{_id}',
            'user_name': f'{username}',
            'idcard': f'{idcard}'
        }
    return {
        'status': 'Not found user'
    }

# ***********************************************************
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

# ***********************************************************

