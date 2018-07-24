from mongoengine import Document, StringField

class Portal(Document):
  name = StringField(max_length=128, required=True, unique=True)