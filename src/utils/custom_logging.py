import datetime
import logging

def configure_log_file(prefix):
  #timestamp = datetime.datetime.now().strftime('%Y%b%d-%H%M%S')
  #log_file = 'logs/' + prefix + '_' + timestamp + '_' + env.upper() + suffix + '.log'
  log_file = 'logs/' + prefix + '.log'
  log_format = '%(levelname)s:%(asctime)s - %(message)s'
  logging.basicConfig(level=logging.INFO, filename=log_file, format=log_format)
  logging.getLogger().addHandler(logging.StreamHandler())
