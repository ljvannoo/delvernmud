import logging
import glob, os

class CommandManager(object):
  class __CommandManager(object):
    def __init__(self):
      self._commands = {}

      self.init_commands('src/commands')

    def init_commands(self, dir):
      os.chdir(dir)
      for file in glob.glob("cmd_*.py"):
        cmd_name = file[4:file.index('.py')]
        self.register_command(cmd_name)

    def register_command(self, cmd_name):
      module_name = 'src.commands.cmd_' + cmd_name
      module = __import__(module_name, fromlist=[''])

      class_name = 'Cmd' + cmd_name.lower().capitalize()
      clazz = getattr(module, class_name)

      command = clazz()
      self._commands[command.name] = command
      logging.info('Registering command \'{0}\''.format(command.name))

    def get(self, cmd_name: str):
      return self._commands[cmd_name]

    # def execute(self, player, cmd_string):
    #   if not cmd_string:
    #     return False

    #   cmd_name = cmd_string
    #   params_string = ''

    #   if ' ' in cmd_name:
    #     parts = cmd_name.split(' ')
    #     cmd_name = parts.pop(0)
    #     params_string = ' '.join(parts)

    #   if cmd_name in self._commands and player.has_command(cmd_name):
    #     command = self._commands[cmd_name]
    #     command.execute(player, params_string)
    #     return True

    #   return False
# -----------------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not CommandManager.instance:
      CommandManager.instance = CommandManager.__CommandManager()
    return CommandManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)