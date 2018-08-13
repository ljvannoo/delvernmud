from src.scripts.logic import Logic
import src.utils.vt100_codes as vt100
from src.managers.character_manager import CharacterManager

class TelnetReporter(Logic):
  def __init__(self, character_id, connection):
    self._character_manager = CharacterManager()

    self._character_id = character_id
    self._connection = connection

  def do_action(self, action):
    if action.action_type == 'enterrealm':
      character = self._character_manager.get_character(self._character_id)
      self.__send_string('{0} enters the realm.'.format(character.name))

  def __send_string(self, msg):
    self._connection.send(msg + vt100.newline)