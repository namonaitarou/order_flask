#設定
class Config(object):
    
    DEBUG=True
    
    SECRET_KEY = "secret_key"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///orderdb.sqlite"
    
    UPLOAD_FOLDER = 'static/img/'