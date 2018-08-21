from src.entities.character import Character, CharacterTemplate

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
      if character_id:
        if character_id not in self._active_characters:
          characters = Character.objects(id=character_id)
          self._active_characters[character_id] = characters[0]

        return self._active_characters[character_id]
      return None

    def get_template(self, template_id):
      if template_id:
        #pylint: disable=E1101
        templates = CharacterTemplate.objects(id=template_id)
        if templates:
          return templates[0]
      return None

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