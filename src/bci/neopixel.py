## SIMULATING THE MATRIX

import numpy as np


class Color:

  def __init__(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue


class NeoPixel:

  def __init__(
      self,
      led_count,
      led_pin,
      led_freq_hz,
      led_dma,
      led_invert,
  ):
    self.led_count = led_count
    self.led_pin = led_pin
    self.led_freq_hz = led_freq_hz
    self.led_dma = led_dma
    self.led_invert = led_invert

    self._pixels = np.zeros(led_count, dtype=Color)

  def begin(self):
    pass

  def setPixelColor(self, index, color):
    self._pixels[index] = color

  def show(self):
    pass
    # for i in range(self.led_count):
    #   print(
    #       f'{i}: {self._pixels[i].red}, {self._pixels[i].green}, {self._pixels[i].blue}'
    #   )

  def numPixels(self):
    return self.led_count
