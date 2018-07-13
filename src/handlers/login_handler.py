import logging
from src.handlers.handler import Handler
from src.handlers.chat_handler import ChatHandler
import src.utils.vt100_codes as vt100
from src.managers.account_manager import AccountManager
from src.utils.exceptions import AccountDoesNotExistException

salt = b'\x1cE\xaa\xefQ\xaa\xee\x856\x95W\xde\x167\x1d\xc8\x0b\x02\x8a\xe8\xb18\x8c\xb6\x95\x8e\x9c\xf5\xbd\x9eq.'

class LoginHandler(Handler):
  def __init__(self, connection):
    super().__init__(connection)
    self._account_manager = AccountManager()
    self._state = 'username'
    self._account = None

  def enter(self):
    self._connection.send(vt100.newline + 'Welcome to BlackPy!!'+ vt100.newline)

    self.prompt()
  
  def prompt(self):
    if self._state == 'username':
      self._connection.send('Account name: ')
    elif self._state == 'password':
      self._connection.send('Password: ')

  def handle(self, cmd):
    if self._state == 'username':
      self.__process_username(cmd)
    elif self._state == 'password':
      self.__process_password(cmd)
  
  def __process_username(self, cmd):
    name = cmd.lower().capitalize()
    self._account = self._account_manager.find_account(name)

    if self._account:
      self._connection.send(vt100.home + vt100.reset)

      self._state = 'password'
      self._connection.set_echo(False)
      
      self.prompt()
    else:
      self._connection.send_blank_line()
      self._connection.send('No account named \'' + vt100.style_name(name) + '\' can be found.' + vt100.newline + vt100.newline)

      self.prompt()

  def __process_password(self, cmd):
    if self._account:
      new_hash = self._account.hash(salt, cmd)
      if new_hash == self._account.password_hash:
        logging.info(vt100.style_name(self._account.name) + ' logged in')
        self._connection.set_echo(True)
      else:
        self._connection.send_blank_line()
        self._connection.send('Incorrect password.' + vt100.newline)
        
    else:
      self._state = 'username'

    self.prompt()
