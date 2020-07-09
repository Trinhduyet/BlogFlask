import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
import math, random 

def save_picture(form_picture):
    '''
        save the profile picture into database name the pictures
        with randomized hax numbers
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 

def send_reset_email(user):
    random_code = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    txt = "code {} author"
    txtbody = txt.format(random_code)
    msg = Message('Password Reset Request',
                  sender='trinhnv.hvitclan@gmail.com',
                  recipients=[user.email])
    msg.body = txtbody
    mail.send(msg)    