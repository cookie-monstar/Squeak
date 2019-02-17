def pad(data):
  return [0]*(24-len(data)) + [1] + data

def unpad(data):
  return data[1+data.index(1):]

def zxor(*z):
  x = 0
  for i in range(len(z)):
    x ^= z[i]
  return x

def xormap(*A):
  return list(map(zxor, *A))

def error(data):
  ebitsrow = [zxor(*[data[5*y+x] for x in range(5)]) for y in range(5)]
  ebitscol = [zxor(*[data[5*x+y] for x in range(5)]) for y in range(5)]
  ebitsdia = [zxor(*[data[5*x+(x+y)%5] for x in range(5)]) for y in range(5)]
  return ebitsrow+ebitscol+ebitsdia

def encode(data, edata=None):
  edata = data if edata == None else edata
  edata = pad(edata)
  data = pad(data)
  message = edata+error(data)
  return message

def decode(message):
  data = message[0:25]
  edata = data[:]
  ebits = xormap(error(data), message[25:])
  count = (sum(ebits), sum(ebits[0:5]), sum(ebits[5:10]), sum(ebits[10:15]))
  if count[0] == 0:
    # errors = 0
    pass
  elif count[1] == count[2] == count[3] == 1:
    # errors = 1
    x = ebits[0:5].index(1)
    y = ebits[5:10].index(1)
    data[5*x+y] ^= 1
  elif count[1] == 0:
    # errors = 2, same row
    y1 = ebits[5:10].index(1)
    y2 = ebits[5:10].index(1,y1+1)
    z1 = ebits[10:15].index(1)
    z2 = ebits[10:15].index(1,z1+1)
    if (y1-z1+5)%5 == (y2-z2+5)%5:
      data[(y1-z1+5)%5*5+y1] ^= 1
      data[(y2-z2+5)%5*5+y2] ^= 1
    else:
      data[(y1-z2+5)%5*5+y1] ^= 1
      data[(y2-z1+5)%5*5+y2] ^= 1
  elif count[2] == 0:
    # errors = 2, same col
    x1 = ebits[0:5].index(1)
    x2 = ebits[0:5].index(1,x1+1)
    z1 = ebits[10:15].index(1)
    z2 = ebits[10:15].index(1,z1+1)
    if (x1+z1)%5 == (x2+z2)%5:
      data[5*x1+(x1+z1)%5] ^= 1
      data[5*x2+(x2+z2)%5] ^= 1
    else:
      data[5*x1+(x1+z2)%5] ^= 1
      data[5*x2+(x2+z1)%5] ^= 1
  elif count[3] == 0:
    # errors = 2, same dia
    x1 = ebits[0:5].index(1)
    x2 = ebits[0:5].index(1,x1+1)
    y1 = ebits[5:10].index(1)
    y2 = ebits[5:10].index(1,y1+1)
    if y1-x1 == y2-x2:
      data[5*x1+y1] ^= 1
      data[5*x2+y2] ^= 1
    else:
      data[5*x1+y2] ^= 1
      data[5*x2+y1] ^= 1
  else:
    # errors = 2
    x1 = ebits[0:5].index(1)
    x2 = ebits[0:5].index(1,x1+1)
    y1 = ebits[5:10].index(1)
    y2 = ebits[5:10].index(1,y1+1)
    z1 = ebits[10:15].index(1)
    z2 = ebits[10:15].index(1,z1+1)
    if (y1-x1+5)%5 in (z1, z2):
      data[5*x1+y1] ^= 1
      data[5*x2+y2] ^= 1
    else:
      data[5*x1+y2] ^= 1
      data[5*x2+y1] ^= 1
  return (unpad(data), unpad(edata))
