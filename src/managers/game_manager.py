import pdb
import time
import queue
import logging
import asyncio

import src.utils.string_utils as string_utils

from src.entities.action import TimedAction, Action, EntityType
from src.managers.region_manager import RegionManager
from src.managers.room_manager import RoomManager
from src.managers.portal_manager import PortalManager
from src.managers.character_manager import CharacterManager
from src.managers.item_manager import ItemManager
from src.managers.command_manager import CommandManager

class GameManager(object):
  class __GameManager(object):
# ----------------------------------------------------------------------
    def __init__(self):
      # Time is in milliseconds
      self._last_query_time = None
      self._running_time = 0

      self._timer_registry = queue.PriorityQueue()

      self._region_manager = RegionManager()
      self._room_manager = RoomManager()
      self._portal_manager = PortalManager()
      self._character_manager = CharacterManager()
      self._item_manager = ItemManager()
      self._command_manager = CommandManager()

      self._connected_characters = []

    def get_connected_characters(self):
      return self._connected_characters

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

    # def add_action_relative(self, relative_time_ms, action_type, entities, data_string):
    #   action = Action(action_type, entities, data_string)
    #   self.add_action_relative(relative_time_ms, action)

    def add_action_relative(self, relative_time_ms, action):
      self.add_action_absolute(self.__system_time_ms() + relative_time_ms, action)

    # def add_action_absolute(self, absolute_time_ms, action_type, entities, data_string):
    #   action = Action(action_type, entities, data_string)
    #   self.add_action_absolute(absolute_time_ms, action)

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
      asyncio.get_event_loop().call_later(.1, self.execute_timed_actions)

    def do_action(self, action):
      # logging.info('Game recieved action: ' + action.action_type)
      if action.action_type == 'chat' or action.action_type == 'announce':
        self.__action_to_realm_players(action)
      elif action.action_type == "do":
        self.__route_action(action)
      elif action.action_type == 'modifyattribute':
        self.__modify_attribute(action)
      elif  action.action_type == 'vision':
        self.__action_to_room_characters(action, action.room_id)
      elif action.action_type == 'enterrealm':
        self.__login(action.character_id)
      elif action.action_type == 'leaverealm':
        self.__logout(action.character_id)
      elif action.action_type == 'attemptsay':
        self.__say(action.character_id, action.data['msg'])
      elif action.action_type == 'command':
        self.__do_command(action.character_id, action.data['cmd']) # TODO: WORKING
      elif action.action_type == 'attemptenterportal':
        self.__enter_portal(action.character_id, action.portal_id) # TODO
      elif action.action_type == 'attempttransport':
        self.__transport(action.character_id, action.room_id)
      elif action.action_type == 'forcetransport':
        self.__transport(action.character_id, action.room_id, force=True)
      # elif action.action_type == 'attemptgetitem':
      #   self.__get_item(action.character_id, action.item_id, action.quantity) # TODO
      # elif action.action_type == 'attemptdropitem':
      #   self.__drop_item(action.character_id, action.item_id, action.quantity) # TODO
      # elif action.action_type ==  'attemptgiveitem':
      #   self.__give_item(action.character_id, action.other_character_id, action.item_id, action.quantity) # TODO
      # elif action.action_type == 'spawnitem':
      #   self.__spawn_item(action.template_id, action.room_id, action.character_id, action.quantity) # TODO
      # elif action.action_type == 'spawncharacter':
      #   self.__spawn_character(action.template_id, action.room_id) # TODO
      # elif action.action_type == 'destroyitem':
      #   self.__destroy_item(action.item_id) # TODO
      # elif action.action_type == 'destroycharacter':
      #   self.__destroy_character(action.character_id) # TODO
      # elif action.action_type == 'cleanup':
      #   self.__cleanup() # TODO
      # elif action.action_type == 'savedatabases':
      #   self.__save_all() # TODO
      # elif action.action_type == 'saveregion':
      #   self.__save_region(action.region_id) # TODO
      # elif action.action_type == 'saveplayers':
        # self.__save_players() # TODO
      # elif action.action_type == 'reloaditems':
      #   self.__reload_item_templates(action.data) # TODO
      # elif action.action_type == 'reloadcharacter':
      #   self.__reload_character_templates(action.data) # TODO
      elif action.action_type == 'reloadregion':
        self.__reload_region(action.data) # TODO
      elif action.action_type == 'reloadcommandscript':
        self.__reload_command_script(action.data) # TODO
      elif action.action_type == 'reloadlogicscript':
        self.__reload_logic_script(action.data) # TODO
      # elif action.action_type == 'messagelogic':
      #   self.__logic_action(action) # TODO
      # elif action.action_type == 'addlogic':
      #   self.__add_logic(action) # TODO
      # elif action.action_type == 'removelogic':
      #   self.__remove_logic(action) # TODO

    def __load_all(self):
      # Is this necesary if the managers load data dynamically from the database?
      pass # TODO

    def __load_timers(self):
      pass # TODO

    def __reload_item_templates(self):
      pass # TODO

    def __reload_charater_templates(self):
      pass # TODO

    def __reload_region(self, name):
      pass # TODO

    def __reload_command_script(self, name):
      pass # TODO

    def __reload_logic_script(self, name):
      pass # TODO

    def __save_all(self):
      pass # TODO

    def __save_players(self):
      pass # TODO

    def save_region(self, region_id):
      pass # TODO

    def __save_timers(self):
      pass # TODO

    def __clean_up(self):
      pass # TODO

    def __transport(self, character_id, room_id, force=False):
      character = self._character_manager.get_character(character_id)
      old_room = self._room_manager.get_room(character.room_id)
      new_room = self._room_manager.get_room(room_id)
      old_region = self._region_manager.get_region(old_room.region_id)
      new_region = self._region_manager.get_region(new_room.region_id)
      changing_regions = old_region.id != new_region.id


      # "ask permission" from the actors to perform the actions
      if not force:
        if changing_regions:
          if old_region.do_action(Action('canleaveregion', character_id=character.id)):
            return

          if new_region.do_action(Action('canenterregion', character_id=character.id)):
            return

          if character.do_action(Action('canleaveregion', region_id=old_region.id)):
            return

          if character.do_action(Action('canenterregion', region_id=new_region.id)):
            return

        if old_room.do_action(Action('canleaveroom', character_id=character.id)):
          return

        if new_room.do_action(Action('canenterroom', character_id=character.id)):
          return

        if character.do_action(Action('canleaveroom', room_id=old_room.id)):
          return

        if character.do_action(Action('canenterroom', room_id=new_room.id)):
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
        old_region.do_action(Action('leaveregion', character_id=character.id))
        character.do_action(Action('leaveregion', region_id=old_region.id))

      action = Action('leaveroom', character_id=character.id, room_id=old_room.id)
      old_room.do_action(action)
      character.do_action(action)
      self.__action_to_room_characters(action, old_room.id)
      self.__action_to_room_items(action, old_room.id)

      if changing_regions:
        action = Action('enterregion', character_id=character.id, room_id=new_region.id)
        new_region.do_action(action)
        character.do_action(action)

      action = Action('enterroom', character_id=character.id, room_id=new_room.id)
      new_room.do_action(action)
      self.__action_to_room_characters(action, new_room.id)
      self.__action_to_room_items(action, new_room.id)

    def __action_to_room_characters(self, action, room_id):
      room = self._room_manager.get_room(room_id)

      for character_id in room.character_ids:
        character = self._character_manager.get_character(character_id)
        if character:
          character.do_action(action)
        else:
          logging.error('do_action() error: character_id "{0}" not found!'.format(character_id))

    def __action_to_room_items(self, action, room_id):
      room = self._room_manager.get_room(room_id)

      for item_id in room.item_ids:
        item = self._item_manager.get_item(item_id)
        item.do_action(action)

    def __action_to_realm_players(self, action):
      for character in self._connected_characters:
        character.do_action(action)

    def __route_action(self, action):
      entity = self.__get_entity_from_action(action)

      if entity:
        entity.do_action(action)

    def __modify_attribute(self, action):
      entity = self.__get_entity_from_action(action)

      if entity:
        for key in action.data:
          entity.data[key] = action.data[key]

    def __get_entity_from_action(self, action):
      entity = None
      if action.target_type == EntityType.REGION:
        entity = self._region_manager.get_region(action.region_id)
      elif action.target_type == EntityType.ROOM:
        entity = self._room_manager.get_room(action.room_id)
      elif action.target_type == EntityType.PORTAL:
        entity = self._portal_manager.get_portal(action.portal_id)
      elif action.target_type == EntityType.CHARACTER:
        entity = self._character_manager.get_character(action.character_id)
      elif action.target_type == EntityType.ITEM:
        entity = self._item_manager.get_item(action.item_id)

      return entity

    def __login(self, character_id):
      character = self._character_manager.get_character(character_id)
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      character.logged_in = True
      self._connected_characters.append(character)
      room.add_character(character_id)
      region.add_character(character_id)

      self.__action_to_realm_players(Action('enterrealm', character_id=character.id))
      region.do_action(Action('enterregion', character_id=character.id))
      character.do_action(Action('enterregion', character_id=character.id))
      room.do_action(Action('enterroom', character_id=character.id))
      self.__action_to_room_characters(Action('enterroom', character_id=character.id), room.id)
      self.__action_to_room_items(Action('enterroom', character_id=character.id), room.id)

    def __logout(self, character_id):
      character = self._character_manager.get_character(character_id)
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      self.__action_to_room_items(Action('leaveroom', character_id=character.id), room.id)
      self.__action_to_room_characters(Action('leaveroom', character_id=character.id), room.id)
      room.do_action(Action('leaveroom', character_id=character.id))
      character.do_action(Action('leaveregion', character_id=character.id))
      region.do_action(Action('leaveregion', character_id=character.id))
      self.__action_to_realm_players(Action('leaverealm', character_id=character.id))

      room.remove_character(character)
      region.remove_character(character)
      self._connected_characters.remove(character)
      character.logged_in = False

    def __say(self, character_id, msg):
      character = self._character_manager.get_character(character_id)
      room = self._room_manager.get_room(character.room_id)
      region = self._region_manager.get_region(room.region_id)

      # ask permission
      action = Action('cansay', character_id=character.id, data={msg: msg})
      if character.do_action(action):
        return
      if room.do_action(action):
        return
      if region.do_action(action):
        return

      # Event notifications
      action = Action('say', character_id=character.id, data={msg: msg})
      self.__action_to_room_characters(action, room.id)
      room.do_action(action)
      region.do_action(action)

    def __enter_portal(self, character_id, portal_id): # TODO: Working
      character = self._character_manager.get_character(character_id)
      portal = self._portal_manager.get_portal(portal_id)
      old_room = self._room_manager.get_room(character.room_id)

      # TODO: I don't understand how paths work, from direction name to entering the portal
      # Do rooms have multiple portals?
      # Do portals have multiple paths with the same direction name?
      paths = portal.find_paths_by_start_room(portal)

    def __do_command(self, character_id: str, cmd_string: str):
      character = self._character_manager.get_character(character_id)

      cmd_name = string_utils.parse_word(cmd_string)
      params = string_utils.remove_word(cmd_string)

      # logging.info('{0} is attempting to execute \'{1}\' with parameters \'{2}\''.format(character.name, cmd_name, params))

      full_command_name = character.find_command(cmd_name)
      if full_command_name:
        command = self._command_manager.get(full_command_name)
        command.execute(character, params)
      else:
        character.do_action(Action("error", data={'msg': 'Unrecognized command: {0}<$nl>'.format(cmd_name)}))


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