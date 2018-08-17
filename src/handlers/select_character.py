import logging
from src.handlers.handler import Handler
from src.handlers.create_character import CreateCharacterHandler
from src.handlers.character_menu import CharacterMenuHandler
from src.managers.character_manager import CharacterManager

class SelectCharacterHandler(Handler):
  def __init__(self, connection, account):
    super().__init__(connection)
    self._character_manager = CharacterManager()
    self._account = account
    self._character_list = []

  def enter(self):
    self._connection.send_blank_line()
    self.__print_menu()
    self.__prompt()

  def handle(self, cmd):
    if not cmd:
      self._connection.leave_handler()
    elif cmd.isdigit() and int(cmd) in range(1,len(self._character_list)+1):
      self._connection.send_blank_line()
      self._connection.switch_handler(CharacterMenuHandler(self._connection, self._account, self._character_list[int(cmd)-1]))
    else:
      self._connection.send_line('<$nl><$red>Invalid option!<$nl>')
      self.__print_menu()
      self.__prompt()

  def __print_menu(self):
    if not self._character_list:
      self.__load_characters()

    self._connection.send_line('You are currently connected to account: {0}'.format(self._account.name))
    menu = """
<$nl>
Your Characters<$nl>
-------------------------------<$nl>
<$nl>"""
    for i in range(len(self._character_list)):
      menu = menu + '{0}) {1}<$nl>'.format(i+1, self._character_list[i].name)
    menu = menu.replace('\n', '')
    self._connection.send_line(menu)

  def __prompt(self):
    self._connection.send('Select a character: ')

  def __load_characters(self):
    characters = self._character_manager.find_by_account(self._account.id)
    for character in characters:
      self._character_list.append(character)