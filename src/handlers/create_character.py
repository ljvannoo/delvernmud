import logging
import src.utils.vt100_codes as vt100
from src.handlers.handler import Handler
from src.entities.character import Character

class CreateCharacterHandler(Handler):
  def __init__(self, connection, account):
    super().__init__(connection)
    self._account = account
    self._state = 'name'

  def enter(self):
    self._connection.send_line(vt100.newline + 'Create a new character: ')
    self._connection.send_blank_line()

    self.prompt()

  def prompt(self):
    if self._state == 'name':
      self._connection.send(vt100.reset + 'Please enter new character name: ')

  def handle(self, cmd):
    name = cmd.lower().capitalize()
    if self.__validate_name(name):
      character = Character()
      character.name = name
      character.account_id = self._account.id
      print('Character name: {0}'.format(character.name))
      character.save()
      self._connection.leave_handler()

  def __validate_name(self, name):
    return True