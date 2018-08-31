from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, ObjectIdField, EmbeddedDocumentField
import src.entities.entity as entity

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

class Room(
    entity.LogicEntity,
    entity.HasData,
    entity.HasRegion,
    entity.HasCharacters,
    entity.HasItems,
    entity.HasPortals):

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)
    self._logic_modules = {}

  coordinates = EmbeddedDocumentField(Coordinate)

  meta: {
    'collection': 'room'
  }