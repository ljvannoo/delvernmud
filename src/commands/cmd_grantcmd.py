import logging

from src.commands.command import Command
from src.managers.command_manager import CommandManager
from src.entities.character import Character
from src.entities.action import Action

class CmdGrantcmd(Command):
  name = 'grantcmd'
  usage = 'grantcmd <cmd_name>'
  description = 'Gives yourself a command.'

  def execute(self, character: Character, param_string: str):
    command_manager = CommandManager()
    cmd_name = param_string.lower().strip()

    if command_manager.valid_command(cmd_name):
      if not character.has_command(cmd_name):
        character.add_command(cmd_name)
        character.do_action(Action('announce', data={'msg': 'You can now use the "{0}" command!<$nl>'.format(cmd_name)}))
        logging.info('{0} granted self command: {1}'.format(character.name, cmd_name))
      else:
        character.do_action(Action('error', data={'msg': 'You already have that command!<$nl>'}))
    else:
      character.do_action(Action('error', data={'msg': 'Invalid command: {0}<$nl>'.format(cmd_name)}))