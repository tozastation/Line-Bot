import peewee

db = peewee.PostgresqlDatabase('dfe7lmrbq8vcjl',
                               host='ec2-54-225-113-161.compute-1.amazonaws.com',
                               user='xndkwheicbgvly',
                               port=5432,
                               password='9ae7ca11594e986db1415eb470e4af59af9271f348ef573dd975e09d8d28398b'
                               )


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Get_Text(BaseModel):
    sentence_id = peewee.IntegerField()
    body = peewee.TextField()


def InitializeDatabase():
    db.drop_tables([Get_Text], safe=True)
    db.create_tables([Get_Text], safe=True)
    db.commit()


if __name__ == '__main__':
    InitializeDatabase(debug=True)