import os

# HOST_SERVERS = "http://0.0.0.0:5000"

PATH_PROJECT = os.path.dirname(__file__)

PATH_MONGO = "mongodb://localhost:27017/" 
UPLOAD_FOLDER = PATH_PROJECT + "/static/img/license-plates"

QR_FOLDER = PATH_PROJECT + "/static/img/qrcode"

MAX_CONTENT_LENGTH = (1000 * 1024) * 10 

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

