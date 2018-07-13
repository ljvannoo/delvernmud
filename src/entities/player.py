class Player(object):
  def __init__(self, model, connection):
    self._model = model
    self._connection = connection
    self._commands = set()

  def __str__(self):
    return '#{1}'.format(self._name)

  def get_name(self):
    return self._model.name

  def get_connection(self):
    return self._connection

  def has_command(self, cmd_name):
    return cmd_name in self._commands
  
  def add_command(self, cmd_name):
    self._commands.add(cmd_name)