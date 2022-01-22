import os
from flask import Flask, request, send_from_directory
import hashlib
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin 
import constants as Const
from imgprocessing import  QR, check_folder

app = Flask(__name__)
cors = CORS(app)

myclient = pymongo.MongoClient(Const.PATH_MONGO)
mydb = myclient['android']
mycol_user = mydb['user']
mycol_log = mydb['log']


@app.route('/')
def index():
    return 'Hello world!'

# ===========SIGNIN/SIGNUP-POST===========
@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    _id = ObjectId()
    username = request.json["username"]
    idcard = request.json['idcard']
    address = request.json['address']
    carnum = request.json['carnum']
    password = request.json['password']
    
    check_folder(Const.QR_FOLDER)

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

    # --------Create QR--------------- 
    link_qr = QR(_id)

    mycol_user.insert_one({
        "_id": _id,
        "username": str(username), 
        "idcard": str(idcard),
        "carnum": str(carnum), 
        "address": str(address), 
        "password": str(password),
        "link_qr": str(link_qr)
    })
    return {
        'status': 'success',
        'qr code': "http://" + request.host + link_qr
    }



@app.route('/signin', methods=['POST'])
@cross_origin()
def signin():
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

@app.route('/log', methods=['POST'])
@cross_origin()
def log():
    _id = request.json["_id"]
    if mycol_log.find_one({"_id": ObjectId(_id)}):
        mycol_log.delete_one({"_id": ObjectId(_id)})
        return {
            "status": "success delete",
        }
    mycol_log.insert_one({"_id": ObjectId(_id)})
    return {
        "status": "success add"
    }


@app.route('/static/<folder>/<name>')
@cross_origin()
def view(folder, name):
    url = Const.PATH_PROJECT + '/static/img/' + folder
    if os.path.exists(url):
        return send_from_directory(f'static/img/{folder}/', name, mimetype='image/gif')
    return {
        "status": "Not Found"
    }

@app.route('/showdb')
@cross_origin()
def showdb():
    data = []
    for x in mycol_user.find({}):
        data.append({
        "_id": str(x['_id']),
        "username": x['username'],
        "idcard": x['idcard'],
        "carnum": x['carnum'], 
        "address": x['address'],
        "password": x['password'],
        "link_qr": x['link_qr']
        })
    return {
        "status": "Success",
        "data": data
    }

# ***********************************************************
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

# ***********************************************************
