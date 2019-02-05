import pyaudio as pa
import numpy as np
import json as js
import time
import math

configFile = open('config.json')
config = js.load(configFile)
configFile.close()

time_span = np.arange(0, 1/config['data_rate'], 1/config['sample_rate'], dtype=np.float)
freq_span = np.asarray(config['freq'], dtype=np.int16)
waves = np.sin(2*np.pi*np.outer(freq_span, time_span))

modulate = lambda bit: waves[bit,:]

audio = pa.PyAudio()

def transmit(raw):
  wave = config['volume']*np.asarray(modulate(raw)).flatten()
  stream = audio.open(format=pa.paFloat32, channels=1, rate=config['sample_rate'], output=True)
  stream.write(wave)
  stream.stop_stream()
  stream.close()

def recieve():
  stream = audio.open(format=pa.paFloat32, channels=1, rate=10000, input=True)
  while True:
    data = stream.read(100, exception_on_overflow=False)
    data = np.fromstring(data, dtype=np.float32)
    data = np.fft.rfft(data)**2
    data = (sum(data[freq_span[0]-5:freq_span[0]+5]), sum(data[freq_span[1]-5:freq_span[1]+5]))
    print('\r%s\r%s\t%s' % (' '*50, data[0], data[1]), end='')