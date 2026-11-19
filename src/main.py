import subprocess
import threading
import logging
from pynput import keyboard
from ocr import MangaOcrEngine
from screen import MacOSCaptureEngine
from processor import OcrProcessor

logging.basicConfig(
   level=logging.DEBUG,
   format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
   datefmt="%H:%M:%S"
)    

logger = logging.getLogger(__name__)

capture_lock = threading.Lock()

ocr_processor = OcrProcessor(MangaOcrEngine(), MacOSCaptureEngine())

def for_canonical(f):
  return lambda k: f(listener.canonical(k))

def copy_to_clipboard(text: str) -> None:
    subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True
    )
    logger.debug(f"Copied '{text}' to clipboard")

def activate_process() -> None:
   threading.Thread(
      target=process_ocr,
      daemon=True
   ).start()

def process_ocr() -> None:
    if not capture_lock.acquire(blocking=False):
        logger.debug("Skipping, process already in use")
        return
    
    try:
        text = ocr_processor.process()

        if text is None:     
            logger.debug("OCR Processor resolved empty text")      
            return None

        copy_to_clipboard(text)
        logger.info(f"OCR Result: {text}")
    except Exception as e:
      logger.exception(f"OCR processing failed: {e}")
    finally:
      capture_lock.release()

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+c'), activate_process
)

with keyboard.Listener(
   on_press=for_canonical(hotkey.press), 
   on_release=for_canonical(hotkey.release)) as listener: listener.join()

