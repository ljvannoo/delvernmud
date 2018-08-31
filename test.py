
class Parent(object):
  def __init__(self):
    self._logic_modules = {}

class Child(Parent):
  def __init__(self):
    super().__init__()

  def print_modules_id(self):
    print(id(self._logic_modules))


def main():
  child1 = Child()
  child1.print_modules_id()
  child2 = Child()
  child2.print_modules_id()
  child1.print_modules_id()

main()