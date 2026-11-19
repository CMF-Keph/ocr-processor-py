from PIL import Image
from manga_ocr import MangaOcr

class MangaOcrEngine:
    def __init__(self):
      self._model = MangaOcr()        
    
    def recognize(self, image: Image.Image) -> str:
        try:
          return self._model(image)
        except Exception as e:
            print(f"Error occurred while recognizing text: {e}")
            return ""