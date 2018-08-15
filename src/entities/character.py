from mongoengine import Document, StringField, ListField, ObjectIdField
import src.entities.entity as entity

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

  def find_command(self, cmd_name: str):
    for command in self.commands:
      if command == cmd_name:
        return command

    for command in self.commands:
      if command.startswith(cmd_name):
        return command
    return None
