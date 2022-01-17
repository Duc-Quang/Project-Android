from genericpath import exists
import os
import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image
import constants as Const
  
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Const.ALLOWED_EXTENSIONS

# compressing an image
def Opt_img(pathfile, s):
      
    # open the image
    picture = Image.open(pathfile)
    
    picture.save(Const.UPLOAD_FOLDER + '/' + str(s) + ".JPEG", 
                 optimize = True, 
                 quality = 10)

    os.remove(pathfile)

    return "/static/images/license-plates/" + str(s) + ".JPEG"
  
def QR(s):
    # Generate QR code
    url = pyqrcode.create(str(s))
    
    # Create and save the png file naming "qr_id.png"
    url.png(Const.QR_FOLDER + f'/qr_{str(s)}.png', scale = 6)

    return '/static/images/qrcode/' + f'qr_{str(s)}.png'

def check_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder, exist_ok=True)
    return
