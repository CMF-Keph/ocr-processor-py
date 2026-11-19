from typing import Protocol
from PIL import Image

class OcrEngine(Protocol):
    def recognize(self, image: Image.Image) -> str:
        ...