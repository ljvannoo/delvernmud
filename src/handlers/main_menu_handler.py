import logging
from src.handlers.handler import Handler

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
    else:
      self._connection.send_line('<$nl><$red>Invalid option!<$nl>')
      self.__print_menu()
      self.__prompt()

  def __prompt(self):
    self._connection.send('Make your selection: ')

  def __print_menu(self):
    self._connection.send_line('You are currently connected to account: {0}'.format(self._account.name))
    menu = """
<$nl>
Account Menu<$nl>
-------------------------------<$nl>
<$nl>
1) Connect to a character <$green>#TODO<$nl>
2) Create a character <$green>#TODO<$nl>
3) Change account password <$green>#TODO<$nl>
4) Delete account <$green>#TODO<$nl>
Q) Quit game<$nl>
            """
    menu = menu.replace('\n', '')
    self._connection.send_line(menu)