class Handler(object):
  def __init__(self, connection):
    self._connection = connection
  
  def enter(self):
    pass
  
  def leave(self):
    pass

  def hang_up(self):
    pass
    
  def prompt(self):
    pass