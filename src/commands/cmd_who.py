from src.commands.base_command import BaseCommand
from src.managers.player_manager import PlayerManager
import src.utils.vt100_codes as vt100

class WhoCommand(BaseCommand):
  def __init__(self):
    super().__init__('who')
    self._player_manager = PlayerManager()

  def execute(self, player, param_string=''):
    conn = player.get_connection()
    
    conn.send_blank_line()
    conn.send(vt100.newline + 'The following players are connected:' + vt100.newline)
    conn.send_blank_line()
    for player_name in self._player_manager.get_player_names():
      conn.send(vt100.cyan + player_name + vt100.newline)

    return True