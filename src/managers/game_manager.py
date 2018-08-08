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

      self._connected_characters = []

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
      self.add_action_relative(relative_time_ms, action)

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
      if action.action_type == 'chat' or action.action_type == 'announce':
        self.__action_to_realm_players(action)
      elif action.action_type == "do":
        self.__route_action(action)
      elif action.action_type == 'modifyattribute':
        self.__modify_attribute(action)
      elif  action.action_type == 'vision':
        self.__action_to_room_characters(action, action.entities['target'])
      elif action.action_type == 'enterrealm':
        self.__login(action.entities['target'])
      elfif action.action_type == 'leaverealm':
        self.__logout(action.entities['target'])
      elif action.action_type == 'attemptsay':
        self.__say(action.entities['target'], action.data_string)
      # TODO Continue implementation of do_action()

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


      # "ask permission" from the actors to perform the actions
      if changing_regions:
        if old_region.do_action('canleaveregion', {character=character}):
          return

        if new_region.do_action('canenterregion', {character=character}):
          return

        if character.do_action('canleaveregion', {region=old_region}):
          return

        if character.do_action('canenterregion', {region=new_region}):
          return

      if old_room.do_action('canleaveroom', {character=character}):
        return

      if new_room.do_action('canenterroom', {character=character}):
        return

      if character.do_action('canleaveroom', {room=old_room}):
        return

      if character.do_action('canenterroom', {room=new_room}):
        return

      # Move the character
      if changing_regions:
        old_region.remove_character(character.id)
        character.region_id = new_region.id
        new_region.add_character(character.id)

      old_room.remove_character(character.id)
      character.room_id = new_room.id
      new_room.add_character(character.id)

      # Notify actors that the event is complete
      if changing_regions:
        old_region.do_action('leaveregion', {character=character})
        character.do_action('leaveregion', {region=old_region})

      action = Action('leaveroom', {character=character, room=old_room})
      old_room.do_action(action)
      character.do_action(action)
      self.__action_to_room_characters(action, old_room)
      self.__action_to_room_items(action, old_room)

      if changing_regions:
        action = Action('enterregion'), {character=character, room=new_region})
        new_region.do_action(action)
        character.do_action(action)

      action = Action('enterroom', {character=character, room=new_room})
      new_room.do_action(action)
      self.__action_to_room_characters(action, new_room)
      self.__action_to_room_items(action, new_room)

    def force_transport(character_id, room_id):
      pass

    #TODO: Implement additional game functions
    def __action_to_room_characters(self, action, room):
      pass

    def __action_to_room_items(self, action, room):
      pass

    def __action_to_realm_players(self, action):
      for character in self._connected_characters:
        character.do_action(action)

    def __route_action(self, action):
      entity = action.entities['target']
      entity.do_action(action)

    def __modify_attribute(self, action):
      entity = action.entities['target']
      entity.data[action.data_key] = action.data_string

    def __login(self, character):
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      character.logged_in = True
      self._connected_characters.append(character)
      room.add_character(character)
      region.add_character(character)

      self.__action_to_realm_players(Action('enterrealm', {character=character}))
      region.do_action(Action('enterregion', {character=character}))
      character.do_action(Action('enterregion', {character=character}))
      room.do_action(Action('enterroom', {character=character}))
      self.__action_to_room_characters(Action('enterroom', {character=character}), room)
      self.__action_to_room_items(Action('enterroom', {character=character}), room)

    def __logout(self, character):
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      self.__action_to_room_items(Action('leaveroom', {character=character}), room)
      self.__action_to_room_characters(Action('leaveroom', {character=character}), room)
      room.do_action(Action('leaveroom', {character=character}))
      character.do_action(Action('leaveregion', {character=character}))
      region.do_action(Action('leaveregion', {character=character}))
      self.__action_to_realm_players(Action('leaverealm', {character=character}))

      room.remove_character(character)
      region.remove_character(character)
      self.__connected_characters.remove(character)
      character.logged_in = False

    def __say(self, character, msg):
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      # ask permission
      action = Action('cansay', {character=character}, data_string=msg)
      if character.do_action(action):
        return
      if room.do_action(action):
        return
      if region.do_action(action):
        return

      # Event notifications
      action = Action('say', {character=character}, data_string=msg)
      self.__action_to_room_characters(action)
      room.do_action(action)
      region.do_action(action)

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