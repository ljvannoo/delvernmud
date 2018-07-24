from mongoengine import Document, StringField, ListField, ObjectIdField, IntField

class Region(Document):
  ref_id = IntField(unique=True, db_field='refId')
  name = StringField(max_length=128)
  keywords = StringField(max_length=128)
  roomIds = ListField(ObjectIdField(), db_field='roomIds')