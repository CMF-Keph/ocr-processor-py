import pytest

from unittest.mock import patch
from PIL import Image

from screen import MacOSCaptureEngine
from subprocess import CompletedProcess

def test_capture_propagates_exception(tmp_path):
    with patch("screen.macos.TEMP_DIR", tmp_path):
        capture_engine = MacOSCaptureEngine()

        with patch("screen.macos.subprocess.run") as mock_run:
            mock_run.return_value = CompletedProcess(args=[], returncode=1)

            with pytest.raises(RuntimeError, match="Screenshot capture failed."):
                capture_engine.capture()
            
            mock_run.assert_called_once_with(["screencapture", "-i", str(tmp_path / "screenshot.png")])

def test_capture_use_cancelation_gives_none(tmp_path):
    with patch("screen.macos.TEMP_DIR", tmp_path):
        capture_engine = MacOSCaptureEngine()

        with patch("screen.macos.subprocess.run") as mock_run:
            mock_run.return_value = CompletedProcess(args=[], returncode=0)            
            result = capture_engine.capture()
    
    assert result is None
    mock_run.assert_called_once_with(["screencapture", "-i", str(tmp_path / "screenshot.png")])

def test_capture_returns_image_when_successful(tmp_path):
    expected_image = Image.new('RGB', (10, 10))

    def fake_screenshot_capture(command):
        expected_image.save(command[-1])
        return CompletedProcess(args=command, returncode=0)

    with patch("screen.macos.TEMP_DIR", tmp_path):
        capture_engine = MacOSCaptureEngine()

        with patch("screen.macos.subprocess.run") as mock_run:
            mock_run.side_effect = fake_screenshot_capture
            result = capture_engine.capture()
            
    assert result is not None
    assert result.size == expected_image.size
    assert result.mode == expected_image.mode
    assert result.tobytes() == expected_image.tobytes()
    mock_run.assert_called_once_with(["screencapture", "-i", str(tmp_path / "screenshot.png")])