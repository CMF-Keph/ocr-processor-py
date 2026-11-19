from unittest.mock import Mock
from PIL import Image

from screen import CaptureEngine
from ocr import OcrEngine
from processor import OcrProcessor

def test_not_call_recognize_image_when_capture_cancelled():
    capture: CaptureEngine = Mock()
    capture.capture.return_value = None
    ocr: OcrEngine = Mock()

    processor = OcrProcessor(ocr, capture)
    result = processor.process()

    assert result is None
    ocr.recognize.assert_not_called()

def test_call_recognize_image_when_capture_success():
    fake_image = Image.new('RGB', (10, 10))

    capture: CaptureEngine = Mock()
    capture.capture.return_value = fake_image
    ocr: OcrEngine = Mock()    
    ocr.recognize.return_value = "こんにちは"

    processor = OcrProcessor(ocr, capture)
    result = processor.process()

    assert result == "こんにちは"
    ocr.recognize.assert_called_once_with(fake_image)