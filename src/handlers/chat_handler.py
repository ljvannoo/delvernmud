import logging

from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100
from src.managers.player_manager import PlayerManager
from src.entities.player import Player

class ChatHandler(Handler):
  def __init__(self, connection):
    super().__init__(connection)
    self._player_manager = PlayerManager()

  def enter(self):
    player = self._connection.player
    self._connection.send_blank_line()
    self._connection.send('Welcome, ' + vt100.green + player.get_name() + vt100.reset + '!' + vt100.newline)
    self._connection.send_blank_line()
    
    self.prompt()
  
  def hang_up(self):
    self._connection.send('\r\nGoodbye!\r\n')

  def prompt(self):
    self._connection.send(vt100.newline + '? ')

  def handle(self, cmd):
    msg = 'You say, "' + cmd + '"' + vt100.newline
    self._connection.send(vt100.newline + msg)

    msg = vt100.green + self._connection.player.get_name() + vt100.reset + ' says, "' + cmd + '"'
    self._player_manager.send_others(self._connection.player, vt100.clearline + vt100.home + msg + vt100.newline)
    logging.info(msg.rstrip())

    self.prompt()
