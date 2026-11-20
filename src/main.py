import subprocess
import threading
import logging
from pynput import keyboard
from ocr import MangaOcrEngine
from screen import MacOSCaptureEngine
from processor import OcrProcessor
from collections.abc import Callable

logger = logging.getLogger(__name__)

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )    

def listen_for_hotkey(on_activate: Callable[[], None]) -> None:
    with keyboard.GlobalHotKeys({
        "<ctrl>+<shift>+c": on_activate
    }) as listener:
        listener.join()

def copy_to_clipboard(text: str) -> None:
    subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True
    )
    logger.debug(f"Copied '{text}' to clipboard")

def process_ocr(ocr_processor: OcrProcessor, capture_lock: threading.Lock) -> None:
    if not capture_lock.acquire(blocking=False):
        logger.debug("Skipping, process already in use")
        return

    try:
        text = ocr_processor.process()

        if text is None:     
            logger.debug("Screencapture probably cancelled")      
            return

        copy_to_clipboard(text)
        logger.info(f"OCR Result: {text}")
    except Exception:
        logger.exception("OCR processing failed")
    finally:
        capture_lock.release()

def main() -> None:
    configure_logging()

    ocr_processor = OcrProcessor(MangaOcrEngine(), MacOSCaptureEngine())
    capture_lock = threading.Lock()

    def start_processing() -> None:
        threading.Thread(
            target=process_ocr,
            args=(ocr_processor, capture_lock),
            daemon=True
        ).start()

    listen_for_hotkey(start_processing)

if __name__ == "__main__":
    main()