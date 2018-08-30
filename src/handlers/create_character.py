import logging
import re
from src.handlers.handler import Handler
from src.entities.character import Character
from src.managers.character_manager import CharacterManager

class CreateCharacterHandler(Handler):
  def __init__(self, connection, account):
    super().__init__(connection)
    self._account = account
    self._character_name = None

  def enter(self):
    self.__prompt()

  def handle(self, cmd):
    if not cmd:
      self._connection.leave_handler()
    elif not self._character_name:
      name = cmd.lower().capitalize()
      if self.__validate_name(name):
        self._character_name = name
        self.__setup()
        self._connection.leave_handler()
        return

    self.__prompt()

  def __setup(self):
    template_id = '5b76f8022ac515cffe5064db'
    character_manager = CharacterManager()
    template = character_manager.get_template(template_id)
    if not template:
      logging.error('Template "{0}" does not exist!'.format(template_id))
      self._connection.send_line('<$red>Error: unable to read template')
      self.__prompt()
      return
    character = Character()
    character.from_template(template)
    character.name = self._character_name
    character.account_id = self._account.id
    character.room_id = '5b7721032ac5150455940919'
    character.region_id = '5b71e3dc2ac51580c8d6baa6'

    character.add_command('look')
    character.add_command('quit')
    character.add_command('who')
    character.add_command('gossip')
    character.add_command('go')

    character.save()

  def __validate_name(self, name):
    character_manager = CharacterManager()
    if re.match('^[a-zA-Z]+$', name) is None:
      self._connection.send_line('<$red>Character names must contain only letters!')
      return False
    elif character_manager.find_by_name(name):
      self._connection.send_line('<$red>Character already exists!')
      return False
    return True

  def __prompt(self):
    if not self._character_name:
      self._connection.send('Please enter new character name: ')