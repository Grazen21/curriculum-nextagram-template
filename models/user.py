from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=False, index=True)
    email = pw.CharField()
    password = pw.CharField()

    def save(self, *arg, **kwarg):
        self.errors=[]
        self.validate()

        if len(self.errors)==0:
            return super(BaseModel, self).save(*arg, **kwarg)
        else:
            return 0 

    
    def validate(self):
        duplicate_username= User.get_or_none(User.username==self.username)

        if duplicate_username:
            self.errors.append('Username not unique')
        

