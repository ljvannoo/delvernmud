import logging

class CommandInterpreter(object):
  def __init__(self):
    self._command_list = dict()

  def register_command(self, cmd_name):
    module_name = 'src.commands.cmd_' + cmd_name
    module = __import__(module_name, fromlist=[''])
    
    class_name = cmd_name.lower().capitalize() + 'Command'
    clazz = getattr(module, class_name)
    
    command = clazz()
    self._command_list[command.get_name()] = command

  def process_command(self, connection, cmd_string):
    executed = False
    for cmd_name in self._command_list:
      cmd = self._command_list[cmd_name]
      executed = cmd.execute(connection, cmd_string)
          
    if executed:
      return True
    
    connection.send('\r\nUnknown command: ' + cmd_string + '\r\n')

    return False