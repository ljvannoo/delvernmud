class Player(object):
  def __init__(self, name):
    self._name = name

  def __str__(self):
    return '#{1}'.format(self._name)

  def get_name(self):
    return self._name