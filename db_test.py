#!/usr/bin/env python3

from mongoengine import connect

import logging  # https://docs.python.org/3/howto/logging.html

from src.utils.custom_logging import configure_log_file
from src.utils.properties import Properties
from src.managers.character_manager import CharacterManager
from src.managers.room_manager import RoomManager
from src.entities.region import Region
from src.entities.room import Room, Coordinate
from src.entities.character import Character, CharacterTemplate
from src.entities.portal import Portal, PortalPath
from src.managers.portal_manager import PortalManager

def main():
  props = Properties()
  props.init_props('properties.yml')

  configure_log_file(props.get('log.prefix'))
  logging.info('******************')

  connect(props.get('db.database'), host='mongodb://' + props.get('db.user') + ':' + props.get('db.password') + '@' + props.get('db.host'))
  logging.info('Connected to database')
  logging.info('Host: %s', props.get('db.host'))
  logging.info('Database: %s', props.get('db.database'))
  logging.info('User: %s', props.get('db.user'))

  props.load_config()

  character_manager = CharacterManager()
  room_manager = RoomManager()

  # character = character_manager.get_character('5b71dc8b2ac5154cbaf5b07f')
  # room = room_manager.get_room('5b71e47c2ac5158358a4f4f5')

  # character.room_id = room.id
  # room.add_character(character)

  # room.save()
  # character.save()

  # region = Region()
  # region.name = 'Starting Region'
  # region.keywords = 'start'
  # region.save()

  # room = Room()
  # room.name = 'Starting Room'
  # room.description = 'You find yourself in an empty room.'
  # room.coordinates = Coordinate(0,0,0)
  # room.region_id = '5b71e3dc2ac51580c8d6baa6'
  # room.save()

  # template = CharacterTemplate()
  # template.name = 'Generic Human'
  # template.region_id = '5b71e3dc2ac51580c8d6baa6'
  # template.save()

  # templates = CharacterTemplate.objects()
  # print(len(templates))
  # for template in templates:
  #   print(template.id)
  # room_manager = RoomManager()

  # start_room = room_manager.get_room('5b7721032ac5150455940919')
  # end_room = room_manager.get_room('5b86a295f230b2181003380f')
  # portal = Portal()
  # portal.name = 'test'
  # portal_path = PortalPath()
  # portal_path.start_room_id = start_room.id
  # portal_path.end_room_id = end_room.id
  # portal_path.direction_name = 'east'
  # portal.paths.append(portal_path)
  # portal.save()

  portal_manager = PortalManager()
  # portal = portal_manager.get_portal('5b86a5502ac51594c8845dfb')
  # print(portal.id)

  room = room_manager.get_room('5b7721032ac5150455940919')
  portal = room.find_portal('east')
  print(portal.id)

main()