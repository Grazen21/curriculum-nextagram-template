from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import Config

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=False, index=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    image_path = pw.CharField(default="")
    role = pw.CharField(default="")

    def save(self, *arg, **kwarg):
        self.errors=[]
        self.validate()

        if len(self.errors)==0:
            return super(BaseModel, self).save(*arg, **kwarg)
        else:
            return 0 

    
    def validate(self):
        duplicate_username= User.get_or_none(User.username==self.username)

        if duplicate_username and duplicate_username != self:
            self.errors.append('Username not unique')
        

    @hybrid_property
    def profile_image_url(self):
        return Config.S3_LOCATION + self.image_path