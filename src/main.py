import subprocess
import threading
from pynput import keyboard

imageToProcessPath: str = "../.temp/screenshot.png"
capture_lock = threading.Lock()

def for_canonical(f):
  return lambda k: f(listener.canonical(k))

def activate_screenshot():
   threading.Thread(
      target=capture_screenshot,
      daemon=True
   ).start()

def capture_screenshot():
    if not capture_lock.acquire(blocking=False):
        return
    
    try:
      print("Capturing screenshot...")   
      subprocess.run(["screencapture", "-i", imageToProcessPath], check=True)
    finally:
      capture_lock.release()

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<shift>+c'), activate_screenshot
)

with keyboard.Listener(
   on_press=for_canonical(hotkey.press), 
   on_release=for_canonical(hotkey.release)) as listener: listener.join()