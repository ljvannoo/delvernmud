import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character
from src.managers.game_manager import GameManager

class CmdWho(Command):
  name = 'who'
  usage = 'who'
  description = 'Shows a list of everyone who is logged in.'

  def execute(self, character: Character, param_string: str):
    game_manager = GameManager()
    connected_characters = game_manager.get_connected_characters()

    msg = 'Players<$nl>----------<$nl>'
    for character in connected_characters:
      msg = msg + '<$cyan>{0}<$reset><$nl>'.format(character.name)

    character.do_action(Action('announce', data={'msg': msg}))