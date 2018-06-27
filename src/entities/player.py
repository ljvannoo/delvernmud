class Player(object):
  def __init__(self, name, connection):
    self._name = name
    self._connection = connection

  def __str__(self):
    return '#{1}'.format(self._name)

  def get_name(self):
    return self._name

  def get_connection(self):
    return self._connection