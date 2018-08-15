import textwrap
import src.utils.vt100_codes as vt100

def wrap(msg, indent=False):
  indent_text = ''

  if indent:
    indent_text = '  '
  return (vt100.newline).join(textwrap.wrap(msg, 80, initial_indent=indent_text))

def indent(msg):
  return '  ' + msg

def parse_word(msg):
  index = msg.find(' ')

  if index > 0:
    return msg[:index]

  return msg

def remove_word(msg):
  word = parse_word(msg)

  if word:
    return msg.replace(word, '').lstrip()

  return msg