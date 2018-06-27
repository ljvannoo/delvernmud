from src.commands.base_command import BaseCommand
from src.managers.player_manager import PlayerManager

class QuitCommand(BaseCommand):
  def __init__(self):
    super().__init__('quit')
    self._player_manager = PlayerManager()

  def execute(self, player, param_string=''):
    self._player_manager.remove_player(player)
    player.get_connection().hang_up()
    
    return True