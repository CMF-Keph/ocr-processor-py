import logging
from PIL import Image
from manga_ocr import MangaOcr

class MangaOcrEngine:
    def __init__(self) -> None:
      self._logger = logging.getLogger(__name__)
      self._model = MangaOcr()        
    
    def recognize(self, image: Image.Image) -> str:        
        self._logger.debug("Processing image with Manga OCR engine")
        return self._model(image)