from src.entities.item import Item

class ItemManager(object):
  class __ItemManager(object):
    def get_portal(self, item_id):
      #pylint: disable=E1101
      return Item.objects(id=item_id)

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not ItemManager.instance:
      ItemManager.instance = ItemManager.__ItemManager()
    return ItemManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)