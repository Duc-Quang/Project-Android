import os
from flask import Flask, request, send_from_directory, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import hashlib
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin 
import constants as Const
from imgprocessing import allowed_file, Opt_img, QR, check_folder

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Const.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Const.MAX_CONTENT_LENGTH
cors = CORS(app)

myclient = pymongo.MongoClient(Const.PATH_MONGO)
mydb = myclient['android']
mycol_user = mydb['user']


@app.route('/')
def index():
    # return 'Hello world!'
    return url_for("signup")

# ===========SIGNIN/SIGNUP-POST===========
@app.route('/signup', methods=['GET', 'POST'])
@cross_origin()
def signup():
    if request.method == 'POST':
        _id = ObjectId()
        username = request.form["username"]
        idcard = request.form['idcard']
        address = request.form['address']
        carnum = request.form['carnum']
        # img license plates
        password = request.form['password']
        
        check_folder(Const.UPLOAD_FOLDER)
        check_folder(Const.QR_FOLDER)

        # ---------------Upload file------------------
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pathfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)

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

        # --------Optimize img-----------
        link_img = Opt_img(pathfile, _id)

        # --------Create QR--------------- 
        link_qr = QR(_id)

        mycol_user.insert_one({
            "_id": _id,
            "username": str(username), 
            "idcard": str(idcard),
            "carnum": str(carnum), 
            "address": str(address), 
            "password": str(password),
            "link_img": str(link_img),
            "link_qr": str(link_qr)
        })
        return {
            'status': 'success',
            'qr code': "https://" + request.host + link_qr
        }
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['POST'])
@cross_origin()
def signin():
    username = request.form['username']
    password = request.form['password']

    x = mycol_user.find_one({"username": username})
    result = hashlib.md5(password.encode())
    password = result.hexdigest()

    if x != None and x['password'] == str(password):
        _id = x['_id']
        idcard = x['idcard']
        link_img = x['link_img']
        return {
            'status': 'success',
            'id_user': f'{_id}',
            'user_name': f'{username}',
            'idcard': f'{idcard}',
            'link_img': "https://" + request.host +  link_img
        }
    return {
        'status': 'Not found user'
    }

@app.route('/static/images/<folder>/<img>')
@cross_origin()
def view_img(folder, img):
    url = Const.PATH_PROJECT + '/static/img'
    if os.path.exists(url):
        return send_from_directory(f'{url}/{folder}/', img, mimetype='image/gif')
    return {
        "status": "Not Found"
    }


# ***********************************************************
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

# ***********************************************************

