class AccountDoesNotExistException(Exception):
  def __init__(self, message):
    super(AccountDoesNotExistException, self).__init__(message)