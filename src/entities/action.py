from enum import Enum

class EntityType(Enum):
  CHARACTER = 0
  ITEM = 1
  ROOM = 2
  PORTAL = 3
  REGION = 4

class Action(object):
  def __init__(self, action_type, target_type=None, region_id=None, room_id=None, portal_id=None, character_id=None, other_character_id=None, item_id=None, quantity=None, template_id=None, data=None):
    self.action_type = action_type
    self.target_type = target_type
    self.region_id = region_id
    self.room_id = room_id
    self.portal_id = portal_id
    self.character_id = character_id
    self.other_character_id = other_character_id
    self.item_id = item_id
    self.quantity = quantity
    self.template_id = template_id
    self.data = data

class TimedAction(object):
  def __init__(self, time=None, action=None):
    self._execution_time = time
    self._action = action
    self.valid = True

  def get_execution_time(self):
    return self._execution_time

  def get_action(self):
    return self._action

  def __eq__(self, other):
    return self.get_execution_time() == other.get_execution_time()

  def __ne__(self, other):
    return self.get_execution_time() != other.get_execution_time()

  def __lt__(self, other):
    return self.get_execution_time() < other.get_execution_time()

  def __le__(self, other):
    return self.get_execution_time() <= other.get_execution_time()

  def __gt__(self, other):
    return self.get_execution_time() > other.get_execution_time()

  def __ge__(self, other):
    return self.get_execution_time() >= other.get_execution_time()

