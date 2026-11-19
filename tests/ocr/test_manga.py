from pathlib import Path
from PIL import Image

from ocr import MangaOcrEngine

def test_recognize_gives_test_when_received_an_image():
  ocr_engine = MangaOcrEngine()

  image_path = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "ocr_test_image.jpg")

  with Image.open(image_path) as image:
    result = ocr_engine.recognize(image)
    assert result == "テスト"