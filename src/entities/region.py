from mongoengine import Document, StringField, ListField, ObjectIdField, IntField
import src.entities.entity as entity

class Region(
    entity.LogicEntity,
    entity.HasData,
    entity.HasCharacters,
    entity.HasItems,
    entity.HasRooms,
    entity.HasPortals):

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)

  keywords = StringField(max_length=128)

  meta: {
    'collection': 'region'
  }