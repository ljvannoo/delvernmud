import textwrap
import src.utils.vt100_codes as vt100

def wrap(msg, indent=False):
  indent_text = ''

  if indent:
    indent_text = '  '
  return (vt100.newline).join(textwrap.wrap(msg, 80, initial_indent=indent_text))

def indent(msg):
  return '  ' + msg