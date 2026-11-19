import subprocess
from PIL import Image
from pathlib import Path
from config import TEMP_DIR

class MacOSCaptureEngine:    
    def __init__(self):
        self._image_path = TEMP_DIR / "screenshot.png"
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    def capture(self) -> Image.Image | None:        
      result = subprocess.run(["screencapture", "-i", str(self._image_path)])

      if result.returncode != 0:
          if not self._image_path.exists():
              return None

          raise RuntimeError("Screenshot capture failed.")
          
      if not self._image_path.exists():
          raise RuntimeError("Screenshot file not found after capture.")
      
      with Image.open(TEMP_DIR / "screenshot.png") as img:
          return img.copy()            
