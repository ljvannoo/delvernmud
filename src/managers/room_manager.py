from src.entities.room import Room

class RoomManager(object):
  class __RoomManager(object):
    def __init__(self):
      self._active_rooms = {}

    def find_by_id(self, id):
      #pylint: disable=E1101
      room = Room.objects(id=id)
      self._active_rooms[room.id] = room
      return room

    def find_by_coordinates(self, x, y, z):
      #pylint: disable=E1101
      room = Room.objects(coordinates__x=x, coordinates__y=y, coordinates__z=z).first()
      self._active_rooms[room.id] = room
      return room

    def find_by_region(self, region_id):
      #pylint: disable=E1101
      return Room.objects(region_id=region_id)

    def get_room(self, room_id):
      if not room_id:
        return None

      #pylint: disable=E1101
      return Room.objects(id=room_id)[0]

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