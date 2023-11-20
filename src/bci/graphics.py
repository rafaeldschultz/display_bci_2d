""" Module for image manipulation.

This module contains the Graphics class, which is responsible for
manipulating images.
"""

from PIL import Image
from pathlib import Path
import errno
import os
import numpy as np


class Graphics:
  """ Graphics class.

  Represents a graphics object.

  Attributes:
    image: The image to be manipulated.
    _view: The image to be shown.
    width: The width of the image.
    height: The height of the image.
    _transformations: The transformations applied to the image.
  
  """

  def __init__(self, asset_path: str) -> None:
    """ Initializes the graphics object.
    
    Args:
      asset_path: The path to the image.
    """
    self._path: str = Path(asset_path)
    self._initialize(asset_path)

  def _initialize(self, asset_path: str) -> None:
    """ Initializes the graphics object.

    Args:
      asset_path: The path to the image.

    Raises:
      FileNotFoundError: If the file is not found.
    """
    if not self._path.exists():
      raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                              asset_path)

    self.image: Image = Image.open(asset_path)
    self._view: Image = self.image.copy()
    self.width: int = self._view.width
    self.height: int = self._view.height
    self._transformations: dict = {'zoom': 1}

  def get_view(self) -> Image:
    """Returns the image to be shown."""
    return self._view

  def get_dimensions(self, view=True) -> tuple:
    """ Returns the dimensions of the image.

    Args:
      view: If True, returns the dimensions of the original image. Otherwise,
        returns the dimensions of the image with current 
        transformations applied.
    """
    return (self.width, self.height) if view else (self.image.width,
                                                   self.image.height)

  def get_filename(self) -> str:
    """ Returns the filename of the image."""
    return self._path.name

  def get_pixels(self):
    """ Returns the pixels of the image."""
    return np.array(self.get_view().getdata())

  def crop(self,
           width: int,
           height: int,
           x: int = 0,
           y: int = 0,
           inplace: bool = False) -> None:
    """ Crops the image.

    Args:
      width: The width of the crop.
      height: The height of the crop.
      x: The x coordinate of the center of the crop.
      y: The y coordinate of the center of the crop.
      inplace: If True, crops the original image. Otherwise, crops the image to
        be shown.
    """

    if not inplace:
      self._view = self.image.crop(
          (x - width, y - height, x + width, y + height))
    else:
      self.image = self.image.crop(
          (x - width, y - height, x + width, y + height))
      self._view = self.image.copy()

  def resize(self,
             width: int,
             height: int,
             keep_aspect_ratio: bool = False,
             inplace: bool = False) -> None:
    """ Resizes the image.

    Args:
      width: The width of the image.
      height: The height of the image.
      keep_aspect_ratio: If True, keeps the aspect ratio of the image.
      inplace: If True, resizes the original image. Otherwise, resizes the image
        to be shown.
    """
    aspect_ratio = width / height

    if keep_aspect_ratio:
      crop_height = self.height
      crop_width = self.width

      if self.width / self.height <= aspect_ratio:
        crop_width = self.height * aspect_ratio

        if crop_width > self.width:
          crop_width = self.width
          crop_height = crop_width / aspect_ratio
      else:
        crop_height = self.width * aspect_ratio

        if crop_height > self.height:
          crop_height = self.height
          crop_width = crop_height / aspect_ratio

      self.crop(int(crop_width), int(crop_height), self.width / 2,
                self.height / 2, inplace)

    if not inplace:
      self._view = self._view.resize((width, height))
    else:
      self.image = self.image.resize((width, height))
      self._view = self._view.resize((width, height))
    self.width = width
    self.height = height

  def zoom(self,
           zoom: int = 2,
           center: bool = True,
           x: int = 0,
           y: int = 0) -> None:
    """ Zooms the image.

    Args:
      zoom: The zoom to be applied.
      center: If True, zooms the image to the center of the image.
      x: The x coordinate of the center of the zoom. It is ignored if center is
        True.
      y: The y coordinate of the center of the zoom. It is ignored if center is
        True.
    """
    if center:
      x = self.width / 2
      y = self.height / 2

    zoom2 = self._transformations['zoom'] * zoom * 2

    if zoom2 <= 1 / 8:
      print('Mínimo zoom atingido.')
      return

    self._transformations['zoom'] *= zoom

    self.crop(self.width / zoom2, self.height / zoom2, x, y)

    self.resize(self.width, self.height)

  def to_ppm(self, path: str = 'assets/pixels.ppm') -> None:
    """ Saves the image as a ppm file.

    Args:
      path: The path to save the image.
    """
    file = Path(path)

    with file.open(mode='w', encoding='utf-8') as f:
      f.write(f'P3\n{self.width} {self.height}\n255\n')

      for pixel in self.get_pixels():
        if pixel[3] == 0:
          f.write('0 0 0\n')
        else:
          f.write(f'{pixel[0]} {pixel[1]} {pixel[2]}\n')
