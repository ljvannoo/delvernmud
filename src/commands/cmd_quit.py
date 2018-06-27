from src.commands.base_command import BaseCommand

class QuitCommand(BaseCommand):
  def __init__(self):
    super().__init__('quit')

  def execute(self, client, cmd_string):
    if cmd_string.lower().startswith('quit'):
      client.hang_up()
      return True

    return False