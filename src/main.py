import subprocess
import threading
import PIL.Image
import os
from manga_ocr import MangaOcr
from pynput import keyboard
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_PATH: Path = PROJECT_DIR / ".temp" / "screenshot.png"

capture_lock = threading.Lock()

print("Initilizing Manga OCR...")
ocr = MangaOcr()
print("Manga OCR ready!")

print("Creating temporary directory for screenshots if not exists...")
os.makedirs(
    os.path.dirname(IMAGE_PATH),
    exist_ok=True
)

print("Press Ctrl + Shift + C to capture a screenshot and perform OCR.")

def for_canonical(f):
  return lambda k: f(listener.canonical(k))

def copy_to_clipboard(text: str):
    subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True
    )

def activate_screenshot():
   threading.Thread(
      target=process_ocr,
      daemon=True
   ).start()


def capture_screenshot() -> bool:
    print("Capturing screenshot...")   
    result = subprocess.run(["screencapture", "-i", IMAGE_PATH], check=True)

    return result.returncode == 0

def process_ocr():
    if not capture_lock.acquire(blocking=False):
        return
    
    try:
      if capture_screenshot():
        image = PIL.Image.open(IMAGE_PATH)
        text = ocr(image)
        copy_to_clipboard(text)
        print("OCR Result:", text)
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

