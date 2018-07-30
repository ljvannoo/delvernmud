from mongoengine import Document, StringField, ListField, ObjectIdField, IntField
import src.entities.entity as entity

class Region(
    entity.LogicEntity, 
    entity.HasData, 
    entity.HasCharacters, 
    entity.HasItems, 
    entity.HasRooms, 
    entity.HasPortals):

  keywords = StringField(max_length=128)

  meta: {
    'collection': 'region'
  }