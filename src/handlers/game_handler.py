from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100
from src.managers.room_manager import RoomManager

class GameHandler(Handler):
  def __init__(self, connection, character):
    super().__init__(connection)
    self._character = character
    self._room_manager = RoomManager()

  def enter(self):
    room = None

    if not self._character.room_id:
      room = self._room_manager.find_by_coordinates(0, 0, 0)
      self._character.room_id = room.id
      self._character.save()
    else:
      room = self._room_manager.find_by_id(self._character.room_id)

    self._connection.send_line(vt100.cyan + room.name)
    self._connection.send_line(room.description)

    self.prompt()

  def hang_up(self):
    self._connection.send(vt100.newline + vt100.bg_magenta + 'Goodbye!' + vt100.newline)

  def prompt(self):
    self._connection.send(vt100.newline + vt100.red + '? ' + vt100.reset)