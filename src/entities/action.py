from enum import Enum

class EntityType(Enum):
  CHARACTER = 0
  ITEM = 1
  ROOM = 2
  PORTAL = 3
  REGION = 4

class Action(object):
  def __init__(self, action_type, entities, data_string=None, data_key=None):
    self._action_type = action_type
    self.entities = entities
    self.data_string = data_string
    self.data_key = data_key

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

