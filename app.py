import os
from flask import Flask, request, send_from_directory
import hashlib
import pymongo
import datetime
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

    # -------------Check exists-------------
    check_username = mycol_user.find_one({"username": str(username)})
    check_idcard = mycol_user.find_one({"idcard": str(idcard)})
    check_carnum = mycol_user.find_one({"carnum": str(carnum)})

    # -----If it found------
    if check_username != None:
        return {
            'status': 'failure',
            'msg': 'username has been exists'
        }
    if check_idcard != None:
        return {
            'status': 'failure',
            'msg': 'idcard has been exists'
        }
    if check_carnum != None:
        return {
            'status': 'failure',
            'msg': 'carnum has been exists'
        }
    
    # ----------hash password----------
    result = hashlib.md5(password.encode())
    password = result.hexdigest()

    # --------Create QR--------------- 
    link_qr = QR(_id)

    # --------add to database---------
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
        'msg': 'Register Successful'
    }

@app.route('/signin', methods=['POST'])
@cross_origin()
def signin():
    username = request.json['username']
    password = request.json['password']

    # --------Check username&password----------
    x = mycol_user.find_one({"username": username})
    result = hashlib.md5(password.encode())
    password = result.hexdigest()

    # ====IF CORRECT====
    if x != None and x['password'] == str(password):
        _id = x['_id']
        idcard = x['idcard']

        return {
            'status': 'success',
            'id_user': f'{_id}'
        }

    # =========IF WRONG=========
    return {
        'status': 'failure',
        'msg': 'Not found user'
    }

# ==========SCAN QR==========
@app.route('/scanqr', methods=['POST'])
@cross_origin()
def scanqr():
    _id = request.json["_id"]

    # ==========if exists in log => delete===========
    if mycol_log.find_one({"_id": ObjectId(_id)}):
        mycol_log.delete_one({"_id": ObjectId(_id)})
        return {
            "status": "success",
            "msg": "Clear data successful"
        }
    
    # =========if not exists in log => add===========
    x = mycol_user.find_one({"_id": ObjectId(_id)})
    username = x["username"]
    time = datetime.datetime.now()
    mycol_log.insert_one({"_id": ObjectId(_id), "time": time, "username": username})

    return {
        "status": "success",
        "data": {
                "_id": str(x['_id']),
                "username": x['username'],
                "idcard": x['idcard'],
                "carnum": x['carnum'], 
                "address": x['address'],
                "link_qr": x['link_qr']
            }
    }

# ============Show QR=============
@app.route('/static/<folder>/<name>')
@cross_origin()
def view(folder, name):
    url = Const.PATH_PROJECT + '/static/img/' + folder
    if os.path.exists(url):
        return send_from_directory(f'static/img/{folder}/', name, mimetype='image/gif')
    return {
        "status": "failure",
        "msg": "Not found"
    }

# ==========SHOW DATABASE============
@app.route('/showdb')
@cross_origin()
def showdb():
    col = request.values.get('col')
    _id = request.values.get('id')

    # ======SHOW DATABSE FOLLOW BY col ("user" & "slot"), id ("number_id")

    if col == None and _id == None:
        return {
            "status": "failure",
            "msg": "Please input collection name"
        }

    if mycol_user.find_one({"_id": ObjectId(_id)}):
        x = mycol_user.find_one({"_id": ObjectId(_id)})
        return {
            "status": "success",
            "data": {
                "_id": str(x['_id']),
                "username": x['username'],
                "idcard": x['idcard'],
                "carnum": x['carnum'], 
                "address": x['address'],
                "link_qr": x['link_qr']
            }
        }
    
    if col == "user":
        data = []
        for x in mycol_user.find({}):
            data.append({
            "_id": str(x['_id']),
            "username": x['username'],
            "idcard": x['idcard'],
            "carnum": x['carnum'], 
            "address": x['address'],
            "link_qr": x['link_qr']
            })
        return {
            "status": "success",
            "data": data
        }

    if col == "slot":
        data = []
        for x in mycol_log.find({}):
            data.append({
            "_id": str(x['_id']),
            "username": x['username'],
            "time": datetime.datetime.strptime(str(x['time']), '%Y-%m-%d %H:%M:%S.%f').ctime()
            })
        return {
            "status": "success",
            "data": data
        }

    else:
        return {
            "status": "failure",
            "msg": "Not found"
        }


# ***********************************************************
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

# ***********************************************************
