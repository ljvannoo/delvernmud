import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character
from src.managers.game_manager import GameManager

class CmdDebug(Command):
  name = 'debug'
  usage = 'debug'
  description = 'Displays some debugg information.'

  def execute(self, character: Character, param_string: str):
    msg = '<$nl>----------<$nl>'
    msg = msg + 'ID: <$green>{0}<$nl>'.format(character.id)
    msg = msg + 'Name: <$green>{0}<$nl>'.format(character.name)
    msg = msg + 'Logged in? <$green>{0}<$nl>'.format(character.logged_in)
    msg = msg + 'Current room: {0}<$nl>'.format(character.room_id)
    msg = msg + '----------<$nl>'
    character.do_action(Action('announce', data={'msg': msg}))