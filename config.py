import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET= os.environ.get("S3_BUCKET_NAME")
    S3_KEY= os.environ.get("S3_ACCESS_KEY")
    S3_SECRET= os.environ.get("S3_SECRET_KEY")
    # S3_LOCATION= 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET) Same as below
    S3_LOCATION= f'http://{S3_BUCKET}.s3-ap-southeast-1.amazonaws.com/'
    # https://grazenbucket.s3-ap-southeast-1.amazonaws.com/
    GOOGLE_CLIENT_ID= os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET= os.environ.get('GOOGLE_CLIENT_SECRET')

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    # GOOGLE_CLIENT_ID= os.environ.get('GOOGLE_CLIENT_ID')
    # GOOGLE_CLIENT_SECRET= os.environ.get('GOOGLE_CLIENT_SECRET')


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
