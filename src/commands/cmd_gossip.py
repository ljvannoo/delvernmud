import logging

from src.commands.base_command import BaseCommand
from src.managers.player_manager import PlayerManager
import src.utils.vt100_codes as vt100

class GossipCommand(BaseCommand):
  def __init__(self):
    super().__init__('gossip')
    self._player_manager = PlayerManager()

  def execute(self, player, param_string=''):
    conn = player.get_connection()
    
    msg = 'You gossip, "' + param_string + '"' + vt100.newline
    conn.send(vt100.newline + msg)

    msg = vt100.cyan + player.get_name() + vt100.reset + ' gossips, "' + param_string + '"'
    self._player_manager.send_others(player, vt100.clearline + vt100.home + msg + vt100.newline)
    logging.info(msg.rstrip())

    return True