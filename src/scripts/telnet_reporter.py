import pdb
import logging

from src.scripts.logic import Logic
import src.utils.vt100_codes as vt100
from src.managers.character_manager import CharacterManager
from src.managers.room_manager import RoomManager
from src.managers.portal_manager import PortalManager
from src.entities.room import Room

class TelnetReporter(Logic):
  def __init__(self, character_id, connection):
    self._character_manager = CharacterManager()
    self._room_manager = RoomManager()
    self._portal_manager = PortalManager()

    self._character_id = character_id
    self._connection = connection

  def do_action(self, action):
    # logging.info('Character {0} recieved action: type={1}'.format(self._character_id, action.action_type))
    if action.action_type == 'enterrealm':
      name = 'You enter'
      if action.character_id != self._character_id:
        character = self._character_manager.get_character(action.character_id)
        name = character.name + ' enters'
      self.__send_line('<$nl>{0} the realm.'.format(name))
    elif action.action_type == 'enterroom':
      if action.character_id and action.character_id == self._character_id:
        self.__see_room(self._room_manager.get_room(action.room_id))
      elif action.data:
        character = self._character_manager.get_character(action.character_id)
        path = action.data['path']
        if path:
          self._connection.send_line('{0} walks in from the {1}.'.format(character.name, path.direction_name))
        else:
          self._connection.send_line('{0} walks in.'.format(character.name))
      self.prompt()
    elif action.action_type == 'leaveroom':
      if action.character_id != self._character_id:
        character = self._character_manager.get_character(action.character_id)
        path = action.data['path']
        if path:
          self._connection.send_line('{0} leaves towards the {1}.'.format(character.name, path.direction_name))
        else:
          self._connection.send_line('{0} walks away.'.format(character.name))
      self.prompt()
    elif action.action_type == 'seeroom':
      if action.character_id and action.character_id == self._character_id:
        self.__see_room(self._room_manager.get_room(action.room_id))
      self.prompt()
    elif action.action_type == 'error':
      self._connection.send('<$bold><$red>' + action.data['msg'])
      self.prompt()
    elif action.action_type == 'leave':
      self._connection.leave_handler()
      self.prompt()
    elif action.action_type == 'announce':
      self._connection.send(action.data['msg'])
      self.prompt()
    elif action.action_type == 'chat':
      character = self._character_manager.get_character(action.character_id)
      name = character.name
      if character.id == self._character_id:
        name = 'You'
      self._connection.send_line('<$nl><$dim><$yellow>{0} gossips, "{1}"<$reset>'.format(name, action.data['msg']))
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
    exits = []
    portal_ids = room.portal_ids
    for portal_id in portal_ids:
      portal = self._portal_manager.get_portal(portal_id)
      for path in portal.paths:
        if path.start_room_id == room.id:
          exits.append(path.direction_name.lower().capitalize())

    if exits:
      self.__send_line('Exits: {0}'.format(', '.join(exits)))

  def __see_room_characters(self, room: Room):
    character_ids = room.character_ids
    for character_id in character_ids:
      if character_id != self._character_id:
        character = self._character_manager.get_character(character_id)
        self.__send_line('{0} is standing here.'.format(character.name))

  def __see_room_items(self, room: Room):
    self.__send_line('No items.') #TODO