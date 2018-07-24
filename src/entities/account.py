from mongoengine import Document, StringField, EmailField
#pylint: disable=E0611
from hashlib import sha3_512

class Account(Document):
  # id
  name = StringField(max_length=128, required=True, unique=True)
  email = EmailField(required=True, unique=True)
  password_hash = StringField(db_field='passwordHash', max_length=128, required=True)

  def hash(self, salt, password):
    hasher = sha3_512()
    hasher.update(salt)
    hasher.update(bytes(password, 'utf-8'))

    return hasher.hexdigest()