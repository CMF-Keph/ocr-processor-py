import subprocess
import logging
from PIL import Image
from config import TEMP_DIR

class MacOSCaptureEngine:    
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._image_path = TEMP_DIR / "screenshot.png"
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    def capture(self) -> Image.Image | None:      
      self._logger.debug("Capturing image with macos's screencapture")
      self._image_path.unlink(missing_ok=True)  # Remove previous screenshot if it exists
      result = subprocess.run(["screencapture", "-i", str(self._image_path)])

      if result.returncode != 0:
          raise RuntimeError("Screenshot capture failed.")
          
      if not self._image_path.exists():
          self._logger.debug("Screenshot capture was cancelled by the user.")
          return None
      
      with Image.open(TEMP_DIR / "screenshot.png") as img:
          self._logger.debug("Image created succesfully")
          return img.copy()            
