class Player(object):
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return '#{1}'.format(self.name)