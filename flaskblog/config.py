import os


class Config:
    SECRET_KEY = 'cfb33786023cc152019e747a051f73c6'  # os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # 設定しなきゃ
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')