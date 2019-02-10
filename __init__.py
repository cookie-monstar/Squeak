from physical import transmit, recieve
from link import encode, decode

class Squeak:
  @staticmethod
  def listen():
    raw = recieve()
    data,edata = decode(raw)
    return Squeak(data, raw, edata)
  @staticmethod
  def squeak(data, edata=None):
    raw = encode(data, edata)
    transmit(raw)
  @classmethod
  def __init__(self, data, raw=None, edata=None):
    self.raw = raw
    self.data = data
    self.edata = edata
    self.repr = ''.join(map(lambda a,b: str(a) if a == b else '\033[32m'+str(a)+'\033[0m' , self.data, self.edata))
  @classmethod
  def __repr__(self):
    return 'Squeak <%s>' % self.repr
