import pytest

from unittest.mock import patch

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

            