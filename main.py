#!/usr/bin/env python3
import logging  # https://docs.python.org/3/howto/logging.html
import asyncio, telnetlib3 # https://telnetlib3.readthedocs.io/en/latest/

from src.utils.custom_logging import configure_log_file

@asyncio.coroutine
def shell(reader, writer):
    writer.write('Would you like to play a game? ')
    inp = yield from reader.read(1)
    if inp:
        writer.echo(inp)
        writer.write('\r\nThey say the only way to win '
                     'is to not play at all.\r\n')
        yield from writer.drain()
    writer.close()

def main():
  configure_log_file('bmud3')
  logging.info('******************')
  logging.info('** Server start **')
  logging.info('******************')

  loop = asyncio.get_event_loop()
  coro = telnetlib3.create_server(port=6023, shell=shell, log=logging.getLogger())
  server = loop.run_until_complete(coro)
  loop.run_until_complete(server.wait_closed())

main()