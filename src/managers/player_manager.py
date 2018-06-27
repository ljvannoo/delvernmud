class PlayerManager(object):
  class __PlayerManager(object):
    def __init__(self):
      self._players = dict()

    def has_player(self, name):
      return (name in self._players)
    
    def add_player(self, player):
      self._players[player.get_name()] = player

    def send_all(self, msg):
      for name in self._players:
        player = self._players[name]
        player.get_connection().send(msg)
      
    def send_others(self, player, msg):
      for name in self._players:
        if name != player.get_name():
          other_player = self._players[name]
          other_player.get_connection().send(msg)
          other_player.get_connection().handler().prompt()
  
  instance = None
  
  def __new__(cls):
    if not PlayerManager.instance:
      PlayerManager.instance = PlayerManager.__PlayerManager()
    return PlayerManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)
  
  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)