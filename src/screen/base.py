from typing import Protocol
from PIL import Image

class CaptureEngine(Protocol):
    def capture(self) -> Image.Image | None:
        ...