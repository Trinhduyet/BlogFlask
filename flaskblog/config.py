import os

class Config:
    # TO-DO MOVE THE KEYS TO .BASH_PROFILE
    SECRET_KEY = '18426b92a85573844291a91f89f3e3e5'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USE_SSL = False
    MAIL_USERNAME = 'trinhnv.hvitclan@gmail.com'
    MAIL_PASSWORD = 'Trangkun2'