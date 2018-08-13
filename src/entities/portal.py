from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, ObjectIdField
import src.entities.entity as entity
# from src.entities.entity import LogicEntity, HasData, HasRegion

class PortalPath(EmbeddedDocument):
  start_room_id = ObjectIdField(db_field='startRoomId')
  end_room_id = ObjectIdField(db_field='endRoomId')
  direction_name = StringField(db_field='directionName')

class Portal(entity.LogicEntity, entity.HasData, entity.HasRegion):
# class Portal(LogicEntity, HasData, HasRegion):
  paths = ListField(EmbeddedDocumentField(PortalPath), db_field='paths')

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)

  def find_paths_by_name(self, portal_name):
    result = []
    for path in self.paths:
      if path.direction_name == portal_name:
        result.append(path)

    return result