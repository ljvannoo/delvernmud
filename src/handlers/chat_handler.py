import logging

from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100

from src.entities.player import Player

from src.managers.player_manager import PlayerManager
from src.managers.command_manager import CommandManager

class ChatHandler(Handler):
  def __init__(self, connection):
    super().__init__(connection)
    self._player_manager = PlayerManager()
    self._command_manager = CommandManager()

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
    player = self._connection.player

    command_executed = self._command_manager.execute(player, cmd)

    if not command_executed:
      self._connection.send(vt100.newline + 'Unknown command' + vt100.newline)

    self.prompt()
