from enum import Enum
import src.utils.vt100_codes as vt100

class Connection(object):
  def __init__(self, reader, writer, notify_queue):
    self._reader = reader
    self._writer = writer
    self.notify_queue = notify_queue
    # self._player = None
    self._handler_stack = []
    self._id = self._writer.get_extra_info('peername')[1]

  def __str__(self):
    return '#{1}'.format(self.get_id())
  
  def get_id(self):
    return self._id

  def current_handler(self):
    if not len(self._handler_stack):
      return None
      
    return self._handler_stack[len(self._handler_stack)-1]

  def enter_handler(self, new_state):
    self._handler_stack.append(new_state)
    new_state.enter()

  def leave_handler(self):
    current_handler = self._handler_stack.pop()
    current_handler.leave()

  def hang_up(self):
    current_handler = self.current_handler()
    self._handler_stack = []
    current_handler.hang_up()

  def send(self, msg):
    self._writer.write(msg)
  
  def send_blank_line(self):
    self._writer.write(vt100.newline)
  
  def echo(self, msg):
    self._writer.echo(msg)

  def readline(self):
    return self._reader.readline()

  def set_iac(self, cmd, opt):
    return self._writer.iac(cmd, opt)

  def close(self):
    self._writer.close()
    
