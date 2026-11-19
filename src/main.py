import subprocess
import threading
from pynput import keyboard
from ocr import MangaOcrEngine
from screen import MacOSCaptureEngine

capture_lock = threading.Lock()

print("Initializing OCR engine...")
ocr_engine = MangaOcrEngine()
capture_engine = MacOSCaptureEngine()
print("OCR engine initialized successfully.")

print("Press Ctrl + Shift + C to capture a screenshot and perform OCR.")

def for_canonical(f):
  return lambda k: f(listener.canonical(k))

def copy_to_clipboard(text: str) -> bool:
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

def process_ocr():
    if not capture_lock.acquire(blocking=False):
        return
    
    try:
      image = capture_engine.capture()
      if image:        
        text = ocr_engine.recognize(image)
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

