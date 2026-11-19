from unittest.mock import patch
from PIL import Image, ImageDraw

from ocr import MangaOcrEngine

def test_recognize_gives_test_when_received_an_image():
  fake_image = Image.new('RGB', (100, 100), color="white")
  draw = ImageDraw.Draw(fake_image)
  draw.text((10,10), "テスト", fill="black")

  ocr_engine = MangaOcrEngine()

  result = ocr_engine.recognize(fake_image)

  assert result == "テスト"