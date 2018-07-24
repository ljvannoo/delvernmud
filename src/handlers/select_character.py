import logging
import src.utils.vt100_codes as vt100
from src.handlers.handler import Handler
from src.handlers.create_character import CreateCharacterHandler
from src.handlers.game_handler import GameHandler
from src.managers.character_manager import CharacterManager

class SelectCharacterHandler(Handler):
  def __init__(self, connection, account):
    super().__init__(connection)
    self._character_manager = CharacterManager()
    self._account = account

  def enter(self):
    self._connection.send_line(vt100.newline + 'Please select a character: ')
    self._connection.send_blank_line()
    self._connection.send_line(vt100.reset + '  C) Create new character')

    self._character_list = []
    characters = self._character_manager.find_by_account(self._account.id)
    for character in characters:
      self._character_list.append(character)

    for i in range(len(self._character_list)):
      self._connection.send_line(vt100.reset + '  ' + str(i+1) + ') ' + self._character_list[i].name)

    self._connection.send_line(vt100.reset + '  Q) Quit')

    self.prompt()

  def prompt(self):
    self._connection.send(vt100.newline + vt100.red + '? ' + vt100.reset)

  def handle(self, cmd):
    if cmd.lower().startswith('c'):
      self._connection.enter_handler(CreateCharacterHandler(self._connection, self._account))
    elif cmd.lower().startswith('q'):
      self._connection.hang_up()
    elif cmd.isdigit() and int(cmd) <= len(self._character_list):
      self._connection.send_blank_line()
      self._connection.enter_handler(GameHandler(self._connection, self._character_list[int(cmd)-1]))
    else:
      self._connection.send(vt100.newline + 'Invalid selection.' + vt100.newline)
      self.prompt()
