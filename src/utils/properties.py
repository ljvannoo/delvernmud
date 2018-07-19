import yaml

from mongoengine import Document, StringField

class Config(Document):
  # id
  key = StringField(max_length=64, required=True, unique=True)
  value = StringField(max_length=20248, required=True)


class Properties(object):
  class __Properties(object):
    def init_props(self, filename):
        with open(filename, 'r') as stream:
            try:
                self._props = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def load_config(self):
        items = Config.objects
        for item in items:
            keys = item.key.split('.')
            self.__insert_prop(keys, self._props, item.value)

    def get(self, propName):
        keys = propName.split('.')
        return self.__find_prop(keys, self._props)

    def __insert_prop(self, keys, props, value):
        key = keys.pop(0)
        if len(keys) == 0:
            props[key] = value
        else:
            if not key in props:
                props[key] = {}
            self.__insert_prop(keys, props[key], value)

    def __find_prop(self, keys, props):
        key = keys.pop(0)
        if len(keys) == 0:
            if key in props:
                return props[key]
            else:
                return None
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