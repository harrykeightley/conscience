from typing import Optional
from PIL.ImageTk import PhotoImage

from director import logger
from PIL.Image import Image


def image_id_path(cache: dict[str, PhotoImage], id: str) -> Optional[str]:
    """Returns the path of this image_id in the cache if it exists, else None"""
    for path, image in cache.items():
        if str(image) == id:
            return path


# TODO: Harry note -> isn't this a glorified dictionary?
class ImageRegistry:
    def __init__(self, images: Optional[dict[str, Image]] = None):
        if images is None:
            self._images = {}
        else:
            self._images = images

    def register_image(self, name: str, image: Image):
        self._images[name] = image

    def lookup(self, name: str) -> Optional[Image]:
        result = self._images.get(name)
        if result is None:
            logger.warn(f"unable to find an image corresponding to {name}")
        return result

    def __contains__(self, name: str) -> bool:
        return name in self._images

    def __getitem__(self, name: str) -> Optional[Image]:
        return self.lookup(name)
