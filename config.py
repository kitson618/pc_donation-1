import os

from webconfig import db, smtp, googlemap, blob, recaptcha, ApplicationInsight

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT') or 'you-will-never-guess'
    RECAPTCHA_PUBLIC_KEY = os.environ.get(
        'RECAPTCHA_PUBLIC_KEY') or recaptcha.RECAPTCHA_SITE_KEY
    RECAPTCHA_PRIVATE_KEY = os.environ.get(
        'RECAPTCHA_PRIVATE_KEY') or recaptcha.SECRET_KEY
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           "mysql+pymysql://" + db.db_user + ':' + db.db_pass + '@' + db.db_host + '/' + db.db_name + "?charset=utf8mb4"

    # for local
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + "?charset=utf8mb4"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or smtp.server
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or smtp.port)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or smtp.user
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or smtp.key
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or smtp.sender
    NGINX_PORT = os.environ.get('NGINX_PORT') or db.web_port
    AZURE_STORAGE_ACCOUNT_NAME = os.environ.get(
        'AZURE_STORAGE_ACCOUNT_NAME') or blob.account_name
    AZURE_STORAGE_ACCOUNT_KEY = os.environ.get(
        'AZURE_STORAGE_ACCOUNT_KEY') or blob.key
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get(
        'AZURE_STORAGE_CONNECTION_STRING') or blob.connect_str
    AZURE_STORAGE_CONTAINER_NAME = os.environ.get(
        'AZURE_STORAGE_CONTAINER_NAME') or blob.container_name
    AZURE_STORAGE_DOMAIN = os.environ.get('AZURE_STORAGE_DOMAIN') or blob.dns
    APPINSIGHTS_INSTRUMENTATIONKEY = os.environ.get(
        'APPINSIGHTS_INSTRUMENTATIONKEY') or ApplicationInsight.key
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['zh', 'en']
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY') or googlemap.google_key
    POSTS_PER_PAGE = 25
