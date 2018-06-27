from src.handlers.handler import Handler

class GameHandler(Handler):
  def enter(self):
    self._connection.send('\r\nYou\'re playing BlackPy!\r\n')
  
  def hang_up(self):
    self._connection.send('\r\nGoodbye!\r\n')

  def prompt(self):
    # self._client.writer.write('\r\x1b[K{}Please enter your name: \r\n'.format(msg))
    self._connection.send('\r\n? ')