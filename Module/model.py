from peewee import *
import os
from playhouse.db_url import connect


url = os.environ['DATABASE_URL']
db = connect(url)


class BaseModel(Model):
    class Meta:
        database = db


class get_user_id(BaseModel):
    user_id = CharField(null=True)


class UserInfomation(BaseModel):
    user_id = TextField(null=True)
    user_name = TextField(null=True)
    user_course = TextField(null=True)


class LogInfomation(BaseModel):
    log_text = TextField(null=True)
    log_owner = TextField(null=True)
    log_status = TextField(null=True)
    log_time = DateTimeField(null=True)


class NoClass(BaseModel):
    status = TextField(null=True)
    class_date = TextField(null=True)
    class_day = TextField(null=True)
    class_time = TextField(null=True)
    class_name = TextField(null=True)
    class_teacher = TextField(null=True)
    class_target = TextField(null=True)
