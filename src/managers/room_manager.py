from src.entities.room import Room

class RoomManager(object):
  class __RoomManager(object):
    def __init__(self):
      pass

    def find_by_id(self, id):
      return Room.objects(id=id)

    def find_by_coordinates(self, x, y, z):
      #pylint: disable=E1101
      return Room.objects(coordinates__x=x, coordinates__y=y, coordinates__z=z).first()

    def find_by_region(self, region_id):
      #pylint: disable=E1101
      return Room.objects(region_id=region_id)

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not RoomManager.instance:
      RoomManager.instance = RoomManager.__RoomManager()
    return RoomManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)