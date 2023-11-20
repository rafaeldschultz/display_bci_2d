"""Main entry point for the application."""

from bci.graphics import Graphics
from bci.display import InternalDisplay, ExternalDisplay

if __name__ == '__main__':

  display_type = 'external'
  image_path = 'assets/ghost.png'
  # image_path = 'assets/pacman.jpg'

  image = Graphics(image_path)
  if display_type == 'internal':
    width, height = image.get_dimensions()
    display = InternalDisplay(width, height)
    display.show(image)
  else:
    display = ExternalDisplay()
    display.show(image)
