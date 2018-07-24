from mongoengine import Document, StringField, ObjectIdField

class Character(Document):
  # id
  name = StringField(max_length=128, required=True, unique=True)
  accountId = ObjectIdField(db_field='accountId')
  room_id = ObjectIdField(db_field='roomId')