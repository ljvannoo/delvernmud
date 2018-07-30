from src.entities.region import Region

class RegionManager(object):
  class __RegionManager(object):
    def __init__(self):
      self._active_regions = {}

    def find_by_id(self, id):
      region = Region.objects(id=id)
      self._active_regions[region.id] = region
      return region

    def get_region(self, region_id):
      self.find_by_id(region_id)
      if region_id in self._active_regions:
        return self._active_regions[region_id]
      else:
        return None

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