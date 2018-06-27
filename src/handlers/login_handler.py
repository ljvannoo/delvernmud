import logging
from src.handlers.handler import Handler
from src.handlers.chat_handler import ChatHandler
import src.utils.vt100_codes as vt100
from src.managers.player_manager import PlayerManager
from src.entities.player import Player

class LoginHandler(Handler):
  def __init__(self, connection):
    super().__init__(connection)
    self._player_manager = PlayerManager()

  def enter(self):
    self._connection.send(vt100.newline + 'Hello, ' + str(self._connection.get_id()) + '!' + vt100.newline)
    self._connection.send(vt100.newline + 'Welcome to BlackPy!!'+ vt100.newline)

    self.prompt()
  
  def prompt(self):
    # self._client.writer.write('\r\x1b[K{}Please enter your name: \r\n'.format(msg))
    self._connection.send('Please enter your name: ')

  def handle(self, cmd):
    name = cmd.lower().capitalize()

    if not self._player_manager.has_player(name):
      player = Player(name, self._connection)
      self._connection.player = player
      self._player_manager.add_player(player)
      
      self._connection.leave_handler()
      self._connection.enter_handler(ChatHandler(self._connection))

      logging.info(vt100.green + name + vt100.reset + ' logged in')
    else:
      self._connection.send_blank_line()
      self._connection.send('That player already exists! Please select a different name.' + vt100.newline)
      self._connection.send_blank_line()

      self.prompt()
