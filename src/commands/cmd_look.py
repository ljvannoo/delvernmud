import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character
from src.managers.room_manager import RoomManager
from src.managers.game_manager import GameManager
import src.utils.string_utils as string_utils

class CmdLook(Command):
  name = 'look'
  usage = 'look <|object|direction>'
  description = 'Looks at the room (default), or at an optional object within the room or a direction.'

  def execute(self, character: Character, param_string: str):
    if not param_string:
      character.do_action(Action('seeroom', character_id=character.id, room_id=character.room_id))
    else:
      room_manager = RoomManager()
      room = room_manager.get_room(character.room_id)
      direction = string_utils.parse_word(param_string)
      portal = room.find_portal(direction)

      game_manager = GameManager()
      game_manager.add_action_absolute(0, Action('attemptseethroughportal', character_id=character.id, portal_id=portal.id, data={'direction': direction}))