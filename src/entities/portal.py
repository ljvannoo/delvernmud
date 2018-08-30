import pdb
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, ObjectIdField
import src.entities.entity as entity

class PortalPath(EmbeddedDocument):
  start_room_id = ObjectIdField(db_field='startRoomId')
  end_room_id = ObjectIdField(db_field='endRoomId')
  direction_name = StringField(db_field='directionName')

class Portal(
    entity.LogicEntity,
    entity.HasData,
    entity.HasRegion):

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)
    self._logic_modules = {}

  paths = ListField(EmbeddedDocumentField(PortalPath), db_field='paths')

  meta: {
    'collection': 'portal'
  }

  def find_path_from(self, start_room_id: str, direction: str):
      for path in self.paths:
        if path.start_room_id == start_room_id and path.direction_name.lower() == direction.lower():
          return path