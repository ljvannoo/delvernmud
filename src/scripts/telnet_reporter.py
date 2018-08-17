import logging

from src.scripts.logic import Logic
import src.utils.vt100_codes as vt100
from src.managers.character_manager import CharacterManager
from src.managers.room_manager import RoomManager
from src.entities.room import Room

class TelnetReporter(Logic):
  def __init__(self, character_id, connection):
    self._character_manager = CharacterManager()
    self._room_manager = RoomManager()

    self._character_id = character_id
    self._connection = connection

  def do_action(self, action):
    # logging.info('Character {0} recieved action: type={1}'.format(self._character_id, action.action_type))
    if action.action_type == 'enterrealm':
      character = self._character_manager.get_character(self._character_id)
      self.__send_line('{0} enters the realm.<$nl>'.format(character.name))
    elif action.action_type == 'seeroom':
      if action.character_id and action.character_id == self._character_id:
        self.__see_room(self._room_manager.get_room(action.room_id))
      self.prompt()
    elif action.action_type == 'error':
      self._connection.send_line('<$bold><$red>' + action.data['msg'])
      self.prompt()
    elif action.action_type == 'leave':
      self._connection.leave_handler()
      self.prompt()
    elif action.action_type == 'announce':
      self._connection.send(action.data['msg'])
      self.prompt()
    elif action.action_type == 'chat':
      character = self._character_manager.get_character(self._character_id)
      self._connection.send_line('<$nl><$dim><$yellow>{0} gossips, "{1}"<$reset>'.format(character.name, action.data['msg']))
      self.prompt()

  def prompt(self):
    self._connection.send('<$nl><$red>?<$reset> ')

  def __send_line(self, msg, indent=False, wrap=False):
    self._connection.send_line(msg, indent, wrap)

  def __see_room(self, room: Room):
    if room:
      self.__see_room_name(room)
      self.__see_room_description(room)
      self.__see_room_exits(room)
      self.__see_room_characters(room)
      self.__see_room_items(room)

  def __see_room_name(self, room: Room):
    self.__send_line('<$cyan>{0}'.format(room.name))

  def __see_room_description(self, room: Room):
    self.__send_line(room.description, indent=True, wrap=True)

  def __see_room_exits(self, room: Room):
    self.__send_line('No exits.') #TODO

  def __see_room_characters(self, room: Room):
    self.__send_line('No characters.') #TODO

  def __see_room_items(self, room: Room):
    self.__send_line('No items.') #TODO