from ocr import OcrEngine
from screen import CaptureEngine

class OcrProcessor:
    def __init__(self, ocr_engine: OcrEngine, capture_engine: CaptureEngine) -> None:
        self._ocr_engine = ocr_engine
        self._capture_engine = capture_engine

    def process(self) -> str | None:
        image = self._capture_engine.capture()

        if image is None:
            return None

        return self._ocr_engine.recognize(image)        