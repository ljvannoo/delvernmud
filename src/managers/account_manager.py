from src.entities.account import Account
from src.utils.exceptions import AccountDoesNotExistException

class AccountManager(object):
  class __AccountManager(object):
    def __init__(self):
      pass

    def find_account(self, name):
      #pylint: disable=E1101
      return Account.objects(name=name).first()


# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not AccountManager.instance:
      AccountManager.instance = AccountManager.__AccountManager()
    return AccountManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)