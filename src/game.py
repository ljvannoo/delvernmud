import contextlib
import asyncio
import telnetlib3
import logging

from src.client import Client, State
from src.command_interpreter import CommandInterpreter

class Game(object):
  def __init__(self):
    self.clients = []
    self._loop = asyncio.get_event_loop()
    self._command_interpreter = CommandInterpreter()

    self._command_interpreter.register_command('quit')

  @contextlib.contextmanager
  def register_link(self, reader, writer):
    client = Client(reader, writer, notify_queue=asyncio.Queue())
    self.clients.append(client)
    try:
      #self.notify_event('LINK ESTABLISHED TO {}'.format(client))
      yield client

    finally:
      self.clients.remove(client)
      #self.notify_event('LOST CONNECTION TO {}'.format(client))

  def main_loop(self, client):
    from telnetlib3 import WONT, ECHO, SGA
    client.writer.iac(WONT, ECHO)
    client.writer.iac(WONT, SGA)
    readline = asyncio.ensure_future(client.reader.readline())
    recv_msg = asyncio.ensure_future(client.notify_queue.get())
    client.writer.write('КОСМОС/300: READY\r\n')
    wait_for = set([readline, recv_msg])
    try:
      while True:
        client.writer.write('? ')

        # await (1) client input or (2) system notification
        done, pending = yield from asyncio.wait(
          wait_for, return_when=asyncio.FIRST_COMPLETED)

        task = done.pop()
        wait_for.remove(task)
        if task == readline:
          # (1) client input
          cmd = (task.result()
               .rstrip())

          client.writer.echo(cmd)
          self._command_interpreter.process_command(client, cmd)

          # await next,
          readline = asyncio.ensure_future(client.reader.readline())
          wait_for.add(readline)

        else:
          # (2) system notification
          msg = task.result()

          # await next,
          recv_msg = asyncio.ensure_future(client.notify_queue.get())
          wait_for.add(recv_msg)

          # show and display prompt,
          client.writer.write('\r\x1b[K{}\r\n'.format(msg))

        if client.state == State.DISCONNECTING:
          if client in self.clients:
            client.writer.close()
            break
    finally:
      for task in wait_for:
        task.cancel()

