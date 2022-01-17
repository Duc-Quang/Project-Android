import os

HOST_SERVERS = "https://0.0.0.0:5000"

PATH_PROJECT = os.path.dirname(__file__)

PATH_MONGO = "mongodb://localhost:27017/" 

UPLOAD_FOLDER = PATH_PROJECT + "/static/img/license-plates"

QR_FOLDER = PATH_PROJECT + "/static/img/qrcode"

MAX_CONTENT_LENGTH = (1000 * 1024) * 8 # 1mb * 8 = 8Mb

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

