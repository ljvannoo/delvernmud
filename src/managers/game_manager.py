import time
import queue

from src.entities.action import TimedAction, Action
from src.managers.character_manager import CharacterManager
from src.managers.room_manager import RoomManager

class GameManager(object):
  class __GameManager(object):
# ----------------------------------------------------------------------
    def __init__(self):
      # Time is in milliseconds
      self._last_query_time = None
      self._running_time = 0

      self._timer_registry = queue.PriorityQueue()
      
      self._character_manager = CharacterManager()
      self._room_manager = RoomManager()

    def __update_time(self):
      if self._last_query_time:
        current_time = self.__system_time_ms()
        self._running_time = self._running_time + (current_time - self._last_query_time)
        
      self._last_query_time = current_time

    def __system_time_ms(self):
      return int(round(time.time() * 1000))

    def get_time(self):
      self.__update_time()
      return self._running_time

    def reset_time(self):
      self.__update_time()
      self._running_time = 0

    def __add_timed_action(self, timed_action):
      if isinstance(timed_action, TimedAction):
        self._timer_registry.put(timed_action)
    
    def add_action_relative(self, relative_time_ms, action_type, entities, data_string):
      action = Action(action_type, entities, data_string)
      self.add_action_relative(relative_time_ms, action):
    
    def add_action_relative(self, relative_time_ms, action):
      self.add_action_absolute(self.__system_time_ms() + relative_time_ms, action)
    
    def add_action_absolute(self, absolute_time_ms, action_type, entities, data_string):
      action = Action(action_type, entities, data_string)
      self.add_action_absolute(absolute_time_ms, action)

    def add_action_absolute(self, absolute_time_ms, action):
      timed_action = TimedAction(self.__system_time_ms(), action)
      self.__add_timed_action(timed_action)

    def execute_timed_actions(self):
      current_time = self.__system_time_ms()

      while not self._timer_registry.empty():
        timed_action = self._timer_registry.get()
        if timed_action.get_execution_time() > current_time:
          self._timer_registry.put(timed_action)
          break
        
        if timed_action.valid:
          self.do_action(timed_action.get_action())
        
    def do_action(self, action):
      pass

    def load_all(self):
      pass

    def load_timers(self):
      pass
      
    def reload_item_templates(self):
      pass
    
    def reload_charater_templates(self):
      pass
    
    def reload_region(self, name):
      pass

    def reload_command_script(self, name):
      pass

    def reload_logic_script(self, name):
      pass

    def save_all(self):
      pass

    def save_players(self):
      pass

    def save_region(self, region_id):
      pass

    def save_timers(self):
      pass

    def clean_up(self):
      pass

    def transport(self, character_id, room_id):
      character = self._character_manager.get_character(character_id)
      old_room = self._room_manager.get_room(character.room_id)
      new_room = self._room_manager.get_room(room_id)
      old_region = self._region_manager.get_region(old_room.region_id)
      new_region = self._region_manager.get_region(new_room.region_id)
      changing_regions = old_region.id != new_region.id

      if changing_regions:
        if(old_region.do_action())
    

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not GameManager.instance:
      GameManager.instance = GameManager.__GameManager()
    return GameManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)