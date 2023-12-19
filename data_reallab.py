from dataclasses import dataclass, field
from itertools import combinations, permutations
import random
from typing import List


@dataclass(frozen=True)
class ModelModule:
    """Class for keeping module information."""
    name: str = ''
    ser: int = ''
    mac: str = ''

    def __init__(self, name, ser, mac):
      self.name = name
      self.ser = ser
      self.mac = mac
      count = 10
      self.MODULE = ('NLS-16DI-Ethernet', 'NLS-8R-Ethernet')
      self.SERs = [random.randint(1, 300) for _ in range(count-1)]
      self.end_MAC = [str(l+h) for l, h in permutations('12345678ABCD', 2)]
      self.MACs = ['70-B3-D5-22-35-'+ str(random.choice(self.end_MAC)) for _ in range(count-1)]

    @staticmethod
    def make_all_module(self):
        return [ModelModule(random.choice(self.MODULE), s, mac) for s in self.SERs for mac in self.MACs]

@dataclass(frozen=True)
class AllModule:
    modules: List[ModelModule] = field(default_factory=ModelModule.make_all_module())
    
    def __repr__(self):
        modules = ', '.join(f'{c!s}' for c in self.modules)
        return f'{self.__class__.__name__}({modules})'



if __name__ == "__main__":


    items = 0


