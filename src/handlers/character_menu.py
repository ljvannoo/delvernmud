import logging
from src.handlers.handler import Handler
from src.handlers.game_handler import GameHandler
from src.managers.character_manager import CharacterManager

class CharacterMenuHandler(Handler):
  def __init__(self, connection, account, character_id):
    super().__init__(connection)
    self._account = account
    self._character_id = character_id
    self._character_manager = CharacterManager()

  def enter(self):
    self._connection.send_line('<$nl>')
    self.__print_menu()
    self.__prompt()

  def hang_up(self):
    self._connection.send_line('<$nl>Goodbye!<$nl>')

  def handle(self, cmd):
    if not cmd:
      self._connection.leave_handler()
    elif cmd == '1':
      self._connection.enter_handler(GameHandler(self._connection, self._account, self._character_id))
    elif cmd == '2':
      #TODO How to delete a character that is referenced by other objects (such as rooms)?
      self.__prompt()
    elif cmd.lower()[:1] == 'q':
      self._connection.hang_up()
    else:
      self._connection.send_line('<$nl><$red>Invalid option!<$nl>')
      self.__print_menu()
      self.__prompt()

  def __print_menu(self):
    character = self._character_manager.get_character(self._character_id)
    self._connection.send_line('You are currently connected to account: {0}'.format(self._account.name))
    self._connection.send_line('You are currently connected to character: {0}'.format(character.name))
    menu = """
<$nl>
Character Menu<$nl>
-------------------------------<$nl>
<$nl>
1) Enter the game<$nl>
2) Delete this character <$green>#TODO<$nl>
Q) Quit the game<$nl>
"""
    menu = menu.replace('\n', '')
    self._connection.send_line(menu)

  def __prompt(self):
    self._connection.send('Make your selection: ')
