# MongoEngine

操作 MongoDB

```py
from mongoengine import connect, Document, StringField, IntField


class Student(Document):
    name = StringField(max_length=16)
    age = IntField(default=1)

    meta = {'collection': 'test_collection'}
    # 自定义 collection 名字


if __name__ == '__main__':
    database = 'test'

    connect(database)

    # insert
    Student.objects.create(name="Hello", age=17)

    # query
    result = Student.objects.filter(name='Hello')

    # delete
    Student.objects.filter(name='Hello').delete()

    # update
    Student.objects.filter(name='Hello').update(name='Hello_new')
```