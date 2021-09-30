#!/usr/bin/env python3

# from OpenSSL import SSL
from flask import *
import cv2
import datetime
import socket

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')


@app.route('/getImage', methods=['GET', 'POST'])
def login():
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

    ret,frame = cap.read()
    x = datetime.datetime.now()
    st=x.strftime('%d_%b_%Y_%H%M%S')+'.bmp'
    if ret:
        cv2.imwrite(st,frame) #save image
    cap.release()
    return send_file(st, mimetype='image/*',as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def default():
    if request.method == 'POST':
        return 'Not supported. You need to access through the mobile app', 401
    else:
        return {'msg': 1}, 200


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


print('\n\nServer running on:', get_ip(),'\n\n')
if __name__ == '__main__':
    app.run('0.0.0.0', 5678, debug=False,)  # ssl_context='adhoc')
