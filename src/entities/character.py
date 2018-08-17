from mongoengine import Document, StringField, ListField, ObjectIdField
import src.entities.entity as entity

class CharacterTemplate(
    entity.LogicEntity,
    entity.HasData,
    entity.HasRegion,
    entity.HasItems):

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)

  meta: {
    'collection': 'characterTemplate'
  }

class Character(
    entity.LogicEntity,
    entity.HasData,
    entity.HasRoom,
    entity.HasRegion,
    entity.HasTemplate,
    entity.HasItems):

  def __init__(self, *args, **kwargs):
    super(Document, self).__init__(*args, **kwargs)

  logged_in = False
  account_id = ObjectIdField(db_field='accountId')
  commands = ListField(StringField())

  meta: {
    'collection': 'character'
  }

  def add_command(self, cmd_name: str):
    if cmd_name not in self.commands:
      self.commands.append(cmd_name)

  def find_command(self, cmd_name: str):
    for command in self.commands:
      if command == cmd_name:
        return command

    for command in self.commands:
      if command.startswith(cmd_name):
        return command
    return None

  def from_template(self, template: CharacterTemplate):
    if template:
      self.name = template.name
      self.description = template.description
      self.logic = template.logic
      self.data = template.data
      self.template_id = template.id
      self.item_ids = template.item_ids
