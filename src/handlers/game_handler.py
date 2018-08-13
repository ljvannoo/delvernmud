from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100
from src.managers.game_manager import GameManager
from src.entities.action import Action
from src.scripts.telnet_reporter import TelnetReporter

class GameHandler(Handler):
  def __init__(self, connection, character):
    super().__init__(connection)
    self._character = character
    self._game_manager = GameManager()

  def enter(self):
    self._character.add_existing_logic(TelnetReporter(self._character.id, self._connection))

    self._game_manager.do_action(Action('enterrealm', character_id=self._character.id))

  def hang_up(self):
    self._connection.send(vt100.newline + vt100.bg_magenta + 'Goodbye!' + vt100.newline)

  def handle(self, cmd_string):
    self._game_manager.do_action(Action('command', character_id=self._character.id, data={'cmd': cmd_string}))

  def prompt(self):
    self._connection.send(vt100.newline + vt100.red + '? ' + vt100.reset)