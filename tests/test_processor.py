import pytest

from unittest.mock import Mock
from PIL import Image

from screen import CaptureEngine
from ocr import OcrEngine
from processor import OcrProcessor

def test_not_call_recognize_image_when_capture_cancelled():
    capture_engine = Mock(spec=CaptureEngine)
    capture_engine.capture.return_value = None
    ocr_engine = Mock(spec=OcrEngine)

    processor = OcrProcessor(ocr_engine, capture_engine)
    result = processor.process()

    assert result is None
    ocr_engine.recognize.assert_not_called()

def test_recognize_image_with_text_when_capture_success():
    fake_image = Image.new('RGB', (10, 10))

    capture_engine = Mock(spec=CaptureEngine)
    capture_engine.capture.return_value = fake_image
    ocr_engine = Mock(spec=OcrEngine)    
    ocr_engine.recognize.return_value = "こんにちは"

    processor = OcrProcessor(ocr_engine, capture_engine)
    result = processor.process()

    assert result == "こんにちは"
    ocr_engine.recognize.assert_called_once_with(fake_image)

def test_propagates_ocr_error():
    fake_image = Image.new('RGB', (10, 10))

    capture_engine = Mock(spec=CaptureEngine)
    capture_engine.capture.return_value = fake_image
    ocr_engine = Mock(spec=OcrEngine)    
    ocr_engine.recognize.side_effect = RuntimeError("OCR Engine Error")

    processor = OcrProcessor(ocr_engine, capture_engine)
    
    with pytest.raises(RuntimeError, match="OCR Engine Error"):
        processor.process()

    capture_engine.capture.assert_called_once()
    ocr_engine.recognize.assert_called_once()

def test_propagates_capture_error():    
    capture_engine = Mock(spec=CaptureEngine)
    capture_engine.capture.side_effect = RuntimeError("Capture Engine Error")
    ocr_engine: OcrEngine = Mock(spec=OcrEngine)        

    processor = OcrProcessor(ocr_engine, capture_engine)
    
    with pytest.raises(RuntimeError, match="Capture Engine Error"):
        processor.process()

    capture_engine.capture.assert_called_once()
    ocr_engine.recognize.assert_not_called()