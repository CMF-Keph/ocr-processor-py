import pytest

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

def test_recognize_image_with_text_when_capture_success():
    fake_image = Image.new('RGB', (10, 10))

    capture: CaptureEngine = Mock()
    capture.capture.return_value = fake_image
    ocr: OcrEngine = Mock()    
    ocr.recognize.return_value = "こんにちは"

    processor = OcrProcessor(ocr, capture)
    result = processor.process()

    assert result == "こんにちは"
    ocr.recognize.assert_called_once_with(fake_image)

def test_ocr_engine_throws_unexpected_error():
    fake_image = Image.new('RGB', (10, 10))

    capture: CaptureEngine = Mock()
    capture.capture.return_value = fake_image
    ocr: OcrEngine = Mock()    
    ocr.recognize.side_effect = RuntimeError("OCR Engine Error")

    processor = OcrProcessor(ocr, capture)
    
    with pytest.raises(RuntimeError, match="OCR Engine Error"):
        processor.process()

def test_capture_engine_throws_unexpected_error():    
    capture: CaptureEngine = Mock()
    capture.capture.side_effect = RuntimeError("Capture Engine Error")
    ocr: OcrEngine = Mock()        

    processor = OcrProcessor(ocr, capture)
    
    with pytest.raises(RuntimeError, match="Capture Engine Error"):
        processor.process()