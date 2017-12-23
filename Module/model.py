from peewee import *

db = PostgresqlDatabase('dfe7lmrbq8vcjl',
                        host='ec2-54-225-113-161.compute-1.amazonaws.com',
                        user='xndkwheicbgvly',
                        port=5432,
                        password='9ae7ca11594e986db1415eb470e4af59af9271f348ef573dd975e09d8d28398b'
                        )


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


if __name__ == 'main':
    unittest.main()