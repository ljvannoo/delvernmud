import logging
from src.handlers.handler import Handler
from src.handlers.create_character import CreateCharacterHandler
from src.handlers.select_character import SelectCharacterHandler

class MainMenuHandler(Handler):
  def __init__(self, connection, account):
    super().__init__(connection)
    self._account = account

  def enter(self):
    self._connection.send_line('<$nl>')
    self.__print_menu()
    self.__prompt()

  def hang_up(self):
    self._connection.send_line('<$nl>Goodbye!<$nl>')

  def handle(self, cmd):
    if cmd.lower()[:1] == 'q':
      self._connection.hang_up()
    elif cmd == '1':
      self.__create_character()
    elif cmd == '2':
      self.__connect_character()
    elif cmd == '3':
      self.__change_password()
    elif cmd == '4':
      self.__delete_account()
    else:
      self._connection.send_line('<$nl><$red>Invalid option!<$nl>')
      self.__print_menu()
      self.__prompt()

  def __create_character(self):
    self._connection.enter_handler(CreateCharacterHandler(self._connection, self._account))

  def __connect_character(self):
    self._connection.enter_handler(SelectCharacterHandler(self._connection, self._account))

  def __change_password(self):
    pass #TODO

  def __delete_account(self):
    pass #TODO

  def __print_menu(self):
    self._connection.send_line('You are currently connected to account: {0}'.format(self._account.name))
    menu = """
<$nl>
Account Menu<$nl>
-------------------------------<$nl>
<$nl>
1) Create a character<$nl>
2) Connect to a character<$nl>
3) Change account password <$green>#TODO<$nl>
4) Delete account <$green>#TODO<$nl>
Q) Quit game<$nl>
            """
    menu = menu.replace('\n', '')
    self._connection.send_line(menu)

  def __prompt(self):
    self._connection.send('Make your selection: ')
