import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character
from src.managers.game_manager import GameManager

class CmdGossip(Command):
  name = 'gossip'
  usage = 'gossip <message>'
  description = 'Send a message to every player who is currently logged into the game.'

  def execute(self, character: Character, param_string: str):
    game_manager = GameManager()

    game_manager.add_action_absolute(0, Action('chat', character_id=character.id, data={'msg': param_string}))