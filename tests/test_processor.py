from unittest.mock import Mock

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