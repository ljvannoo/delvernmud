from mongoengine import Document, StringField, ObjectIdField, ListField, DictField
# from src.managers.portal_manager import PortalManager
from src.entities.action import Action

class Entity(Document):
  #id
  name = StringField(max_length=128, required=True, unique=True)
  description = StringField(max_length=2048)

  meta = {'allow_inheritance': True, 'abstract': True}

class LogicEntity(Entity):
  logic = ListField(db_field='logic')

  meta = {'allow_inheritance': True, 'abstract': True}

  def add_logic(self, logic_name):
    pass # TODO

  def add_existing_logic(self, logic):
    logic_name = type(logic).__name__
    self._logic_modules[logic_name] = logic

    if logic_name not in self.logic:
      self.logic.append(logic_name)

  def remove_logic(self, logic_name):
    pass # TODO

  def has_logic(self, logic_name):
    pass # TODO

  def get_logic(self, name):
    return self._logic_modules[name]

  def do_action(self, action):
    for logic_name in self._logic_modules:
      logic = self._logic_modules[logic_name]
      result = logic.do_action(action)
      if result != None:
        return result

    return None

  def do_action_helper(self, action_type, entities, data_string):
    action = Action(action_type, entities, data_string)
    self.do_action(action)

class HasData(Document):
  data = DictField(db_field='data')

  meta = {'allow_inheritance': True, 'abstract': True}

class HasRegion(Document):
  region_id = ObjectIdField(db_field='regionId')

  meta = {'allow_inheritance': True, 'abstract': True}

class HasRoom(Document):
  room_id = ObjectIdField(db_field='roomId')

  meta = {'allow_inheritance': True, 'abstract': True}

class HasRooms(Document):
  room_ids = ListField(ObjectIdField(), db_field='roomIds')

  meta = {'allow_inheritance': True, 'abstract': True}

class HasTemplate(Document):
  template_id = ObjectIdField(db_field='templateId')
  
  meta = {'allow_inheritance': True, 'abstract': True}

class HasCharacters(Document):
  character_ids = ListField(ObjectIdField(), db_field='characterids')

  meta = {'allow_inheritance': True, 'abstract': True}

  def add_character(self, character_id: str):
    if character_id not in self.character_ids:
      self.character_ids.append(character_id)

  def remove_character(self, character_id: str):
    if character_id in self.character_ids:
      self.character_ids.remove(character_id)

class HasItems(Document):
  item_ids = ListField(ObjectIdField(), db_field='itemIds')
  
  meta = {'allow_inheritance': True, 'abstract': True}

class HasPortals(Document):
  portal_ids = ListField(ObjectIdField(), db_field='portalIds')
  
  meta = {'allow_inheritance': True, 'abstract': True}

  # def find_portals_by_name(self, portal_name):
  #   portal_manager = PortalManager()

  #   portals = []
  #   for portal_id in self.portal_ids:
  #     portal = portal_manager.get_portal(portal_id)
  #     if portal.find_path_by_name(portal_name):
  #       portals.append(portal)

  #   return portals