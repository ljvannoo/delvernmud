import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character

class CmdLook(Command):
  name = 'look'
  usage = 'look <|object>'
  description = 'Looks at the room (default, r at an option object within the room.'

  def execute(self, character: Character, param_string: str):
    character.do_action(Action('seeroom', character_id=character.id, room_id=character.room_id))