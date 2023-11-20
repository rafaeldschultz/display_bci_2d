""" Display module.

This module contains the display classes.

Classes:
  _Display: Represents a generic display to show graphics.
  InternalDisplay: Represents a display to show graphics in a window.
  ExternalDisplay: Represents a display to show graphics in a LED matrix.
"""

import tomllib
from abc import ABC, abstractmethod
from pathlib import Path
from tkinter import Label, Tk

from munch import munchify
from PIL import ImageTk
from pynput import keyboard

from bci.graphics import Graphics
from bci.neopixel import Color, NeoPixel

# from rpi_ws281x import Adafruit_NeoPixel


class _Display(ABC):
  """Display class.

  Represents a generic display to show graphics.

  Attributes:
    height: The height of the display.
    width: The width of the display.
    _graphics: The graphics to be shown.
  """

  def __init__(self, width: int, height: int) -> None:
    """ Initializes the display.

    Args:
      width: The width of the display.
      height: The height of the display.
    
    Raises:
      ValueError: If height or width are less than or equal to zero.
    """

    if height <= 0 or width <= 0:
      raise ValueError('Height and width must be greater than zero.')

    self.height: int = height
    self.width: int = width
    self._graphics: Graphics = None

  @abstractmethod
  def update(self) -> None:
    """Updates the display."""
    pass

  @abstractmethod
  def show(self) -> None:
    """Shows the graphics in the display."""
    pass

  def add_zoom(self, zoom: int = 2, zoom_out: bool = False) -> None:
    """ Adds zoom to the graphics being shown.

    Args:
      zoom: The zoom to be added.
      zoom_out: If the zoom should be added or subtracted.
    """
    if zoom_out:
      self._graphics.zoom(1 / zoom)
    else:
      self._graphics.zoom(zoom)
    self.update()


class InternalDisplay(_Display):
  """Internal Display class.

  Represents a display to show graphics in a window.

  Attributes:
    height: The height of the display.
    width: The width of the display.
    _graphics: The graphics to be shown.
    _frame: The window of the display.
    _panel: The panel of the display to show the graphics.
  """

  def __init__(self, width: int, height: int) -> None:
    """ Initializes the Internal Display.

    Args:
      width: The width of the display.
      height: The height of the display.
    """
    super().__init__(width, height)
    self._initialize()

  def _initialize(self) -> None:
    """ Initializes the window and the panel of the display."""
    self._frame = Tk()
    self._frame.geometry(f'{self.width}x{self.height}')
    self._panel = None

  def _bind_events(self) -> None:
    """ Binds the events of the display.
    
    Raises:
      ValueError: If the frame is not initialized.
    """
    if self._frame is None:
      raise ValueError('Frame is not initialized.')

    self._frame.bind('<KP_Add>', lambda _: self.add_zoom())
    self._frame.bind('<KP_Subtract>', lambda _: self.add_zoom(zoom_out=True))

  def show(self, graphics: Graphics) -> None:
    """ Shows the graphics in the display.

    Args:
      graphics: The graphics to be shown.
    """
    self._graphics = graphics
    self._bind_events()
    self._frame.title(graphics.get_filename())

    photo_image = ImageTk.PhotoImage(graphics.get_view())
    self._panel = Label(image=photo_image)
    self._panel.image = photo_image
    self._panel.pack(side='bottom', fill='both', expand='yes')

    self._frame.mainloop()

  def update(self) -> None:
    """ Updates the display.

    Raises:
      ValueError: If the panel is not initialized.
    """
    if self._panel is None:
      raise ValueError('Panel is not initialized.')

    photo_image = ImageTk.PhotoImage(self._graphics.get_view())
    self._panel.configure(image=photo_image)
    self._panel.image = photo_image


class ExternalDisplay(_Display):
  """ External Display class.

  Represents a display to show graphics in a LED matrix.

  Attributes:
    height: The height of the display.
    width: The width of the display.
    _graphics: The graphics to be shown.
    _frame: The LED matrix.
    _display_config: The display configuration.
  """

  def __init__(self, config_path: str = 'settings/led_matrix.toml') -> None:
    """ Initializes the External Display.
    
    Args:
      config_path: The path of the configuration file.
    """
    self._load_config(config_path)
    super().__init__(self._display_config.width_count,
                     self._display_config.height_count)
    self._initialize()

  def _initialize(self) -> None:
    """ Initializes the LED matrix."""
    self._frame = NeoPixel(self._display_config.led_count,
                           self._display_config.gpio_pin,
                           self._display_config.led_freq_hz,
                           self._display_config.led_dma,
                           self._display_config.led_invert)
    self._frame.begin()
    # self._frame = Adafruit_NeoPixel(self._display_config.led_count,
    #                                 self._display_config.gpio_pin,
    #                                 self._display_config.led_freq_hz,
    #                                 self._display_config.led_dma,
    #                                 self._display_config.led_invert,
    #                                 self._display_config.led_brightness)

    # self._frame.begin()

  def _load_config(self, path: str):
    """ Loads the display configuration.

    Args:
      path: The path of the configuration file.
    
    Raises:
      FileNotFoundError: If the configuration file is not found.
    """
    config_file = Path(path)
    if not config_file.is_file():
      raise FileNotFoundError(f'Could not find config file: {path}')

    with config_file.open(mode='rb') as f:
      self._display_config = munchify(tomllib.load(f)['specs'])

  def show(self, graphics: Graphics) -> None:
    """ Shows the graphics in the display.

    Args:
      graphics: The graphics to be shown.
    """
    self._graphics = graphics

    self._graphics.resize(self.width,
                          self.height,
                          keep_aspect_ratio=True,
                          inplace=True)

    self._graphics.to_ppm()

    pixels = self._graphics.get_pixels()
    for i in range(self._frame.numPixels()):
      self._frame.setPixelColor(i,
                                Color(pixels[i][0], pixels[i][1], pixels[i][2]))

    self._frame.show()
    self._bind_events()

  def _bind_events(self) -> None:
    """ Binds the events of the display."""
    try:
      while True:
        with keyboard.Listener(on_press=self._on_press) as listener:
          listener.join()
    except KeyboardInterrupt:
      print('Finalizando...')

  def _on_press(self, key):
    """ Handles the key press event.

    Args:
      key: The key pressed.
    """
    try:
      if key.char == '+':
        self.add_zoom()
        self.update()
      elif key.char == '-':
        self.add_zoom(zoom_out=True)
        self.update()
    except AttributeError:
      pass

  def update(self) -> None:
    """ Updates the display."""
    pixels = self._graphics.get_pixels()
    for i in range(self._frame.numPixels()):
      self._frame.setPixelColor(i,
                                Color(pixels[i][0], pixels[i][1], pixels[i][2]))

    self._frame.show()
    self._graphics.to_ppm()
