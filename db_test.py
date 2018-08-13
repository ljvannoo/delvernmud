#!/usr/bin/env python3

from mongoengine import connect

import logging  # https://docs.python.org/3/howto/logging.html

from src.utils.custom_logging import configure_log_file
from src.utils.properties import Properties
from src.managers.character_manager import CharacterManager
from src.managers.room_manager import RoomManager
from src.entities.region import Region
from src.entities.room import Room, Coordinate

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

  character = character_manager.get_character('5b71dc8b2ac5154cbaf5b07f')
  room = room_manager.get_room('5b71e47c2ac5158358a4f4f5')

  character.room_id = room.id
  room.add_character(character)

  room.save()
  character.save()

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

main()