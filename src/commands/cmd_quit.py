import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character

class CmdQuit(Command):
  name = 'quit'
  usage = 'look'
  description = 'Removes you from the game and takes you back to the game menu.'

  def execute(self, character: Character, param_string: str):
    character.do_action(Action('leave', character_id=character.id))