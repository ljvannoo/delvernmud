from enum import Enum
import src.utils.vt100_codes as vt100
import src.utils.string_utils as string_utils

class Connection(object):
  def __init__(self, reader, writer, notify_queue):
    self._reader = reader
    self._writer = writer
    self.notify_queue = notify_queue
    # self._player = None
    self._handler_stack = []
    self._id = self._writer.get_extra_info('peername')[1]
    self.player = None

  def __str__(self):
    return '#{1}'.format(self.get_id())

  def get_id(self):
    return self._id

  def handler(self):
    if not len(self._handler_stack):
      return None

    return self._handler_stack[len(self._handler_stack)-1]

  def enter_handler(self, new_state):
    self._handler_stack.append(new_state)
    new_state.enter()

  def leave_handler(self):
    current_handler = self._handler_stack.pop()
    current_handler.leave()
    self.handler().enter()

  def hang_up(self):
    current_handler = self.handler()
    self._handler_stack = []
    current_handler.hang_up()
    self.close()

  def send(self, msg, indent=False, wrap=False):
    new_msg = self.__translate_colors(msg)
    if wrap:
      new_msg = string_utils.wrap(new_msg, indent=indent)

    self._writer.write(new_msg)

  def send_line(self, msg, indent=False, wrap=False):
    self.send(msg, indent=indent, wrap=wrap)
    self.send_blank_line()

  def send_blank_line(self):
    self._writer.write(vt100.newline)

  def echo(self, msg):
    self._writer.echo(self.__translate_colors(msg))

  def readline(self):
    return self._reader.readline()

  def set_iac(self, cmd, opt):
    return self._writer.iac(cmd, opt)

  def set_echo(self, echo):
    from telnetlib3 import WONT, WILL, ECHO
    if echo:
      self.set_iac(WONT, ECHO)
    else:
      self.set_iac(WILL, ECHO)

  def close(self):
    self._writer.close()

  def __translate_colors(self, msg):
    index = msg.find('<')
    new_msg = msg

    while index >= 0:
      end_index = new_msg.find('>')
      if end_index >= 0:
        type_indicator = new_msg[index + 1]
        if type_indicator == '$':
          new_msg = self.__translate_string_color(index, end_index, new_msg)
        elif type_indicator == '#':
          new_msg = self.__translate_number_color(index, end_index, new_msg)
      index = new_msg.find('<', index + 1)

    return new_msg

  def __translate_string_color(self, start_index, end_index, msg):
    color_tag = msg[start_index:end_index+1]
    vt100_color = None

    if color_tag == '<$black>':
      vt100_color = vt100.black
    elif color_tag == '<$red>':
      vt100_color = vt100.red
    elif color_tag == '<$green>':
      vt100_color = vt100.green
    elif color_tag == '<$yellow>':
      vt100_color = vt100.yellow
    elif color_tag == '<$blue>':
      vt100_color = vt100.blue
    elif color_tag == '<$magenta>':
      vt100_color = vt100.magenta
    elif color_tag == '<$cyan>':
      vt100_color = vt100.cyan
    elif color_tag == '<$white>':
      vt100_color = vt100.white
    elif color_tag == '<$bold>':
      vt100_color = vt100.bold
    elif color_tag == '<$dim>':
      vt100_color = vt100.dim
    elif color_tag == '<$reset>':
      vt100_color = vt100.reset
    elif color_tag == '<$nl>':
      vt100_color = vt100.newline

    if vt100_color:
      return msg.replace(color_tag, vt100_color)

    return msg

  def __translate_number_color(self, start_index, end_index, msg):
    return msg #TODO
