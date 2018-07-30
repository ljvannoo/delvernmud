from mongoengine import Document, StringField, ObjectIdField, ListField, DictField
from src.entities.action import Action

class Entity(Document):
  #id
  name = StringField(max_length=128, required=True, unique=True)
  description = StringField(max_length=2048)

  meta = {'allow_inheritance': True}

class LogicEntity(Entity):
  logic_data = DictField(db_field='logic_data')
  
  meta = {'allow_inheritance': True}

  def get_logic(self, name):
    return self.logic_data[name]

  # TODO: Overloading doesn't work this way in Python...
  def do_action(self, action):
    pass

  def do_action(self, action_type, entities, data_string):
    action = Action(action_type, entities, data_string)
    self.do_action(action)
    
class HasData(Document):
  data = DictField(db_field='data')

  meta = {'allow_inheritance': True}

class HasRegion(Document):
  region_id = ObjectIdField(db_field='regionId')

  meta = {'allow_inheritance': True}

class HasRoom(Document):
  room_id = region_id = ObjectIdField(db_field='roomId')
  
  meta = {'allow_inheritance': True}

class HasRooms(Document):
  room_ids = ListField(ObjectIdField(), db_field='roomIds')
  
  meta = {'allow_inheritance': True}

class HasTemplate(Document):
  template_id = ObjectIdField(db_field='templateId')
  
  meta = {'allow_inheritance': True}

class HasCharacters(Document):
  character_ids = ListField(ObjectIdField(), db_field='characterids')
  
  meta = {'allow_inheritance': True}

class HasItems(Document):
  item_ids = ListField(ObjectIdField(), db_field='itemIds')
  
  meta = {'allow_inheritance': True}

class HasPortals(Document):
  portal_ids = ListField(ObjectIdField(), db_field='portalIds')
  
  meta = {'allow_inheritance': True}