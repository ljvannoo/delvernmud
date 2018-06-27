from src.handlers.handler import Handler
import src.utils.vt100_codes as vt100

class GameHandler(Handler):
  def enter(self):
    self._connection.send(vt100.newline + 'You\'re playing BlackPy!' + vt100.newline)
  
  def hang_up(self):
    self._connection.send(vt100.newline + vt100.bg_magenta + 'Goodbye!' + vt100.newline)

  def prompt(self):
    # self._client.writer.write('\r\x1b[K{}Please enter your name: \r\n'.format(msg))
    self._connection.send(vt100.newline + '? ')