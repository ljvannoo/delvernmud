import yaml

class Properties(object):
  class __Properties(object):
    def __init__(self):
        pass

    def init_props(self, filename):
        with open(filename, 'r') as stream:
            try:
                self._props = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get(self, propName):
        keys = propName.split('.')
        return self.__find_prop(keys, self._props)

    def __find_prop(self, keys, props):
        key = keys.pop(0)
        if(len(keys) == 0):
            return props[key]
        return self.__find_prop(keys, props[key])


# ----------------------------------------------------------------------
  instance = None

  def __new__(cls):
    if not Properties.instance:
      Properties.instance = Properties.__Properties()
    return Properties.instance

  def __getattr__(self, name):
    return getattr(self.instance, name)

  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)