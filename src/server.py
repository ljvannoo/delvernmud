from telnetlib3 import TelnetServer

class Server(TelnetServer):
  def on_timeout(self):
    print('It is done!')
    self.writer.close()