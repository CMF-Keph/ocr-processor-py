from PIL import Image
from manga_ocr import MangaOcr

class MangaOcrEngine:
    def __init__(self) -> None:
      self._model = MangaOcr()        
    
    def recognize(self, image: Image.Image) -> str:
        return self._model(image)