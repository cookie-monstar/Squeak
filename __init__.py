from physical import transmit, recieve
from link import encode, decode

class Squeak:
  @staticmethod
  def listen():
    raw = recieve()
    data = decode(raw)
    return Squeak(data, raw)
  @staticmethod
  def squeak(data):
    raw = encode(data)
    transmit(raw)
  @staticmethod
  def weak_squeak():
    pass
  @classmethod
  def __init__(self, data, raw=None):
    self.raw = raw
    self.data = data if type(data) is str else ''.join(data)
  @classmethod
  def __repr__(self):
    return 'Squeak{%s}' % self.data
