from src.entities.portal import Portal

class PortalManager(object):
  class __PortalManager(object):
    def get_portal(self, portal_id):
      #pylint: disable=E1101
      return Portal.objects(id=portal_id)

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