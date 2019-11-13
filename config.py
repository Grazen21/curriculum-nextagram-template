import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    # S3_BUCKET = os.environment.get("S3_BUCKET_NAME")
    # S3_KEY = os.environment.get("S3_ACCESS_KEY")
    # S3_SECRET = os.environment.get("S3_SECRET_KEY")
    # S3_LOCATION =''.format(S3_BUCKET)


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


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
