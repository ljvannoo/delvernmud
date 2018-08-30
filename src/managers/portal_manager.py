from src.entities.portal import Portal

class PortalManager(object):
  class __PortalManager(object):
    def __init__(self):
      self._active_portals = {}

    def get_portal(self, portal_id):
      if portal_id:
        if portal_id not in self._active_portals:
          #pylint: disable=E1101
          portals = Portal.objects(id=portal_id)
          self._active_portals[portal_id] = portals[0]

        return self._active_portals[portal_id]
      return None

# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not PortalManager.instance:
      PortalManager.instance = PortalManager.__PortalManager()
    return PortalManager.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)