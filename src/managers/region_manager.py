from src.entities.region import Region

class RegionManager(object):
  class __RegionManager(object):
    def __init__(self):
      self._active_regions = {}

    def get_region(self, region_id):
      if not region_id:
        return None

      #pylint: disable=E1101
      return Region.objects(id=region_id)[0]

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not RegionManager.instance:
      RegionManager.instance = RegionManager.__RegionManager()
    return RegionManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)