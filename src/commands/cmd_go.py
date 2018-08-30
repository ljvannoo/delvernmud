import logging

from src.commands.command import Command
from src.entities.action import Action
from src.entities.character import Character
from src.managers.game_manager import GameManager
from src.managers.room_manager import RoomManager

class CmdGo(Command):
  name = 'go'
  usage = 'go <exit>'
  description = 'Tries to move your character into a portal.'

  def execute(self, character: Character, param_string: str):
    if not param_string:
      character.do_action(Action('error', data={'msg': 'Please specify a direction!<$nl>'}))
      return

    room_manager = RoomManager()
    room = room_manager.get_room(character.room_id)

    portal = room.find_portal(param_string)
    game_manager = GameManager()

    game_manager.add_action_absolute(0, Action('attemptenterportal', character_id=character.id, portal_id=portal.id, data={'direction': param_string}))