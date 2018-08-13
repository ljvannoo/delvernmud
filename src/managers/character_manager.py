from src.entities.character import Character

class CharacterManager(object):
  class __CharacterManager(object):
    def __init__(self):
      self._active_characters = {}

    def find_by_name(self, name):
      #pylint: disable=E1101
      return Character.objects(name=name).first()

    def find_by_account(self, account_ref):
      #pylint: disable=E1101
      return Character.objects(account_id=account_ref)

    def get_character(self, character_id):
      # if character_id in self._active_characters:
      #   return self._active_characters[character_id]
      # else:
      #   return None

      if not character_id:
        return None
        
      #pylint: disable=E1101
      return Character.objects(id=character_id)[0]

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not CharacterManager.instance:
      CharacterManager.instance = CharacterManager.__CharacterManager()
    return CharacterManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)