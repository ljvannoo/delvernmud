from src.entities.player import Player
# from src.utils.exceptions import PlayerDoesNotExistException
# from src.entities.models import PlayerModel

class PlayerManager(object):
  class __PlayerManager(object):
    def __init__(self):
      self._connected_players = {}

    # def is_connected(self, player_name):
    #   return player_name.lower() in self._connected_players

    # def get_connected_player(self, player_name):
    #   if self.is_connected(player_name):
    #     return self._connected_players[player_name]

    #   return None

    # def connect_player(self, player_name, connection):
    #   model = PlayerModel.objects.filter(name=player_name)
    #   if not model:
    #     raise PlayerDoesNotExistException(player_name + ' does not exist!')

    #   player = Player(model, connection)
    #   self._connected_players[player.get_name()] = player

    #   player.add_command('quit')
    #   player.add_command('who')
    #   player.add_command('gossip')

    #   return player

    # def get_player_names(self):
    #   return self._connected_players

    # def send_all(self, msg):
    #   for name in self._connected_players:
    #     player = self._connected_players[name]
    #     player.get_connection().send(msg)
      
    # def send_others(self, player, msg):
    #   for name in self._connected_players:
    #     if name != player.get_name():
    #       other_player = self._connected_players[name]
    #       other_player.get_connection().send(msg)
    #       other_player.get_connection().handler().prompt()

    # def remove_player(self, player):
    #   del self._connected_players[player.get_name()]
  
  instance = None
  
  def __new__(cls):
    if not PlayerManager.instance:
      PlayerManager.instance = PlayerManager.__PlayerManager()
    return PlayerManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)
  
  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)