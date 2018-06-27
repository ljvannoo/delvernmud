class PlayerManager(object):
  class __PlayerManager(object):
    def __init__(self):
      self._players = dict()

    def has_player(self, name):
      return (name in self._players)
    
    def add_player(self, player):
      self._players[player.get_name()] = player
  
  instance = None
  
  def __new__(cls):
    if not PlayerManager.instance:
      PlayerManager.instance = PlayerManager.__PlayerManager()
    return PlayerManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)
  
  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)