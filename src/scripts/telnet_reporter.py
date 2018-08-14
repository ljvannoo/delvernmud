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
    logging.info('Character {0} recieved action: type={1}'.format(self._character_id, action.action_type))
    if action.action_type == 'enterrealm':
      character = self._character_manager.get_character(self._character_id)
      self.__send_line('{0} enters the realm.'.format(character.name))
    elif action.action_type == 'seeroom':
      if action.character_id and action.character_id == self._character_id:
        self.__see_room(self._room_manager.get_room(action.room_id))

  def __send_line(self, msg):
    self._connection.send(msg + vt100.newline)

  def __see_room(self, room: Room):
    if room:
      self.__see_room_name(room)
      self.__see_room_description(room)
      self.__see_room_exits(room)
      self.__see_room_characters(room)
      self.__see_room_items(room)

  def __see_room_name(self, room: Room):
    self.__send_line(room.name)

  def __see_room_description(self, room: Room):
    self.__send_line(room.description)

  def __see_room_exits(self, room: Room):
    self.__send_line('No exits.') #TODO

  def __see_room_characters(self, room: Room):
    self.__send_line('No characters.') #TODO

  def __see_room_items(self, room: Room):
    self.__send_line('No items.') #TODO