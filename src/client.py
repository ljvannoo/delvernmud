from enum import Enum

class State(Enum):
  CONNECTED = 1
  DISCONNECTING = 2

class Client(object):
  def __init__(self, reader, writer, notify_queue):
    self.reader = reader
    self.writer = writer
    self.notify_queue = notify_queue
    self._player = None
    self.state = State.CONNECTED

  def __str__(self):
    return '#{1}'.format(*self.writer.get_extra_info('peername'))