import subprocess
import threading
import PIL.Image
import os
from pynput import keyboard
from pathlib import Path
from ocr import MangaOcrEngine

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_PATH: Path = PROJECT_DIR / ".temp" / "screenshot.png"

capture_lock = threading.Lock()

print("Initializing OCR engine...")
ocr_engine = MangaOcrEngine()
print("OCR engine initialized successfully.")

print("Creating temporary directory for screenshots if not exists...")
os.makedirs(
    os.path.dirname(IMAGE_PATH),
    exist_ok=True
)

print("Press Ctrl + Shift + C to capture a screenshot and perform OCR.")

def for_canonical(f):
  return lambda k: f(listener.canonical(k))

def copy_to_clipboard(text: str) -> bool:
    result = subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True
    )

    return result.returncode == 0

def activate_screenshot():
   threading.Thread(
      target=process_ocr,
      daemon=True
   ).start()


def capture_screenshot() -> bool:
    print("Capturing screenshot...")   
    result = subprocess.run(["screencapture", "-i", IMAGE_PATH])

    return result.returncode == 0

def process_ocr():
    if not capture_lock.acquire(blocking=False):
        return
    
    try:
      if capture_screenshot():
        image = PIL.Image.open(IMAGE_PATH)
        text = ocr_engine.recognize(image)
        if copy_to_clipboard(text):           
          print("OCR Result:", text)
        else:
          print("Failed to copy text to clipboard.")
    except Exception as e:
      print(f"OCR processing failed: {e}")
    finally:
      capture_lock.release()

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+c'), activate_screenshot
)

with keyboard.Listener(
   on_press=for_canonical(hotkey.press), 
   on_release=for_canonical(hotkey.release)) as listener: listener.join()

