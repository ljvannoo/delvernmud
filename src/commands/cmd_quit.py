from src.commands.base_command import BaseCommand
from src.client import State

class QuitCommand(BaseCommand):
  def __init__(self):
    super().__init__('quit')

  def execute(self, client, cmd_string):
    if cmd_string.lower().startswith('quit'):
      client.state = State.DISCONNECTING
      return True

    return False

