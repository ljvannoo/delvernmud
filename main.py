#!/usr/bin/env python3

from mongoengine import connect

import logging  # https://docs.python.org/3/howto/logging.html
import asyncio, telnetlib3 # https://telnetlib3.readthedocs.io/en/latest/


from src.utils.custom_logging import configure_log_file
from src.game import Game

PORT = 6023
game = Game()

connect('blackpy')

def shell(reader, writer):
    global game
    with game.register_link(reader, writer) as client:
        yield from game.main_loop(client)

def main():
    configure_log_file('bmud3')
    logging.info('******************')
    logging.info('** Server started on 127.0.0.1:6023')
    
    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=PORT, log=logging.getLogger(), shell=shell)
    server = loop.run_until_complete(coro)
    loop.run_until_complete(server.wait_closed())
    
main()