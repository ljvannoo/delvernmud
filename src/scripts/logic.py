from src.scripts.script import Script

class Logic(Script):
  name = None

  def can_save(self):
    return True

  def get_attribute(self, name):
    return None

  def do_action(self, action):
    return None