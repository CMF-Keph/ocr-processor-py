import subprocess
from PIL import Image
from config import TEMP_DIR

class MacOSCaptureEngine:    
    def __init__(self) -> None:
        self._image_path = TEMP_DIR / "screenshot.png"
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    def capture(self) -> Image.Image | None:      
      self._image_path.unlink(missing_ok=True)  # Remove previous screenshot if it exists
      result = subprocess.run(["screencapture", "-i", str(self._image_path)])

      if result.returncode != 0:
          raise RuntimeError("Screenshot capture failed.")
          
      if not self._image_path.exists():
          print("Screenshot capture was cancelled.")
          return None
      
      with Image.open(TEMP_DIR / "screenshot.png") as img:
          return img.copy()            
