import os
import pyqrcode
import png
import constants as Const
  
def QR(s):
    # Generate QR code
    url = pyqrcode.create(str(s))
    
    # Create and save the jpeg file naming "qr_id.jpeg"
    url.png(Const.QR_FOLDER + f'/qr_{str(s)}.png', scale = 6)

    return '/static/qrcode/' + f'qr_{str(s)}.png'

def check_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder, exist_ok=True)
    return
