import subprocess
from PIL import Image
from pathlib import Path

class MacOSCaptureEngine:
    def __init__(self):
        project_directory = Path(__file__).resolve().parent
        self._image_path: Path = project_directory / ".temp" / "screenshot.png"
        self._image_path.parent.mkdir(parents=True, exist_ok=True)
    
    def capture(self) -> Image.Image | None:        
      result = subprocess.run(["screencapture", "-i", str(self._image_path)])

      if result.returncode != 0:
          if not self._image_path.exists():
              return None

          raise RuntimeError("Screenshot capture failed.")
          
      if not self._image_path.exists():
          raise RuntimeError("Screenshot file not found after capture.")
      
      with Image.open(self._image_path) as img:
          return img.copy()            
