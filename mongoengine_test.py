#!/usr/bin/env python3

from mongoengine import *


class TestDocument(Document):
  name = StringField(required=True)
  email = StringField(required=True)

  meta = {'collection': 'test_account'}

connect('blackpy')

# test = TestDocument(name='john', email='john@example.com')
# test.save()

for doc in TestDocument.objects:
  print(str(doc.id) + ' ' + doc.name)