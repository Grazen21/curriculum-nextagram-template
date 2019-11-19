from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from config import Config

class Images(BaseModel, UserMixin):
    images= pw.CharField()
    user_id= pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_url(self):
        return Config.S3_LOCATION + self.images