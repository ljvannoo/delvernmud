from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100
from src.managers.game_manager import GameManager
from src.managers.character_manager import CharacterManager
from src.entities.action import Action
from src.scripts.telnet_reporter import TelnetReporter

class GameHandler(Handler):
  def __init__(self, connection, account, character_id):
    super().__init__(connection)
    self._account = account
    self._character_id = character_id
    self._game_manager = GameManager()
    self._character_manager = CharacterManager()

  def enter(self):
    character = self._character_manager.get_character(self._character_id)
    character.add_existing_logic(TelnetReporter(self._character_id, self._connection))

    self._game_manager.do_action(Action('enterrealm', character_id=self._character_id))
    character.do_action(Action('seeroom', character_id=self._character_id, room_id=character.room_id))
    # self.prompt()

  def hang_up(self):
    self._connection.send(vt100.newline + vt100.bg_magenta + 'Goodbye!' + vt100.newline)

  def handle(self, cmd_string):
    self._game_manager.do_action(Action('command', character_id=self._character_id, data={'cmd': cmd_string.strip()}))
    # self.prompt()