from typing import Protocol
from PIL import Image
from pathlib import Path

class CaptureEngine(Protocol):
    def capture(self) -> Image.Image | None:
        ...