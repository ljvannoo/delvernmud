#!/usr/bin/env python3

from mongoengine import connect

import logging  # https://docs.python.org/3/howto/logging.html
import asyncio, telnetlib3 # https://telnetlib3.readthedocs.io/en/latest/


from src.utils.custom_logging import configure_log_file
from src.utils.properties import Properties
from src.game import Game
from src.managers.game_manager import GameManager

PORT = None
game = None

def shell(reader, writer):
    global game
    with game.register_link(reader, writer) as client:
        yield from game.main_loop(client)

def main():
    global game
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

    game = Game()
    game_manager = GameManager()

    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=props.get('server.port'), log=logging.getLogger(), shell=shell, timeout=0)
    server = loop.run_until_complete(coro)
    logging.info('Server started on 127.0.0.1:' + str(props.get('server.port')))
    loop.call_later(1, game_manager.execute_timed_actions)
    loop.run_until_complete(server.wait_closed())

main()