from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, ObjectIdField, EmbeddedDocumentField

# class RoomTemplate(Document):
#   name = StringField(max_length=128, required=True, unique=True)
#   description = StringField(max_length=2048)
#   region_id = ObjectIdField(db_field='regionId')
#   portal_template_ids = ListField(ObjectIdField(), db_field='portalTemplateIds')
#   character_template_ids = ListField(ObjectIdField(), db_field='characterTemplateIds')
#   item_template_ids = ListField(ObjectIdField(), db_field='itemTemplateIds')

class Coordinate(EmbeddedDocument):
  x = IntField(required=True) # West to East
  y = IntField(required=True) # south to north
  z = IntField(required=True) # bottom to top

class Room(Document):
  name = StringField(max_length=128, required=True, unique=True)
  description = StringField(max_length=2048)
  # template_id = ObjectIdField()
  coordinates = EmbeddedDocumentField(Coordinate)
  region_id = ObjectIdField(db_field='regionId')
  portal_ids = ListField(ObjectIdField(), db_field='portalIds')
  character_ids = ListField(ObjectIdField(), db_field='characterIds')
  item_ids = ListField(ObjectIdField(), db_field='itemIds')