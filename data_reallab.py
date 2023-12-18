from dataclasses import dataclass

@dataclass
class Module:
    """Class for keeping module information."""
    name: str 
    ser: int
    mac: str

    def __init__(self, name, ser, mac):
      self.name = name
      self.ser = ser
      self.mac = mac


if __name__ == "__main__":
    module = Module('NLS-16DI-Ethernet', 123, '70-B3-D5-22-34-6F')
    print(module)