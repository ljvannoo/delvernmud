from src.entities.character import Character
class Command(object):
  usage = None
  description = None

  def execute(self, character: Character, param_string: str):
    pass