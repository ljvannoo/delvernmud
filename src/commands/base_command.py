class BaseCommand(object):
  def __init__(self, name):
    self._name = name
  
  def get_name(self):
    return self._name

  def execute(self, client, cmd_string):
    pass