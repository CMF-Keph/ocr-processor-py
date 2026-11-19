import subprocess

imageToProcessPath: str = "../.temp/screenshot.png"

subprocess.run(["screencapture", "-i", imageToProcessPath], check=True)


