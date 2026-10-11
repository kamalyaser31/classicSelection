"""Unit tests for classicSelection add-on."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

addon_dir = str(Path(__file__).parent / "addon")
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)


def setUpModule() -> None:
    # Stub NVDA modules if not present in test environment
    class DummyGlobalPlugin:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def terminate(self) -> None:
            pass

    for mod in [
        "addonHandler",
        "api",
        "inputCore",
        "logHandler",
        "scriptHandler",
        "textInfos",
        "ui",
        "globalCommands",
    ]:
        if mod not in sys.modules:
            mock = MagicMock()
            if mod == "scriptHandler":
                mock.script = lambda **kwargs: (lambda f: f)
            elif mod == "textInfos":
                mock.UNIT_CHARACTER = 1
            sys.modules[mod] = mock

    if "globalPluginHandler" not in sys.modules:
        gph = MagicMock()
        gph.GlobalPlugin = DummyGlobalPlugin
        sys.modules["globalPluginHandler"] = gph


class TestClassicSelection(unittest.TestCase):
    def setUp(self) -> None:
        import globalPlugins.classicSelection as cs

        self.cs = cs
        self.plugin = cs.GlobalPlugin()

    def tearDown(self) -> None:
        self.plugin.terminate()

    def test_lifecycle(self) -> None:
        self.assertIsNone(self.plugin._copyStartMarker)
        self.assertIsNone(self.plugin._copyStartMarkerObj)

    def test_calculateSelectionRange_forward(self) -> None:
        start_marker = MagicMock()
        curr_pos = MagicMock()

        copy_instance = MagicMock()
        start_marker.copy.return_value = copy_instance

        # Forward cursor movement
        curr_pos.compareEndPoints.return_value = 1
        copy_instance.compareEndPoints.return_value = 1

        result = self.plugin._calculateSelectionRange(start_marker, curr_pos)
        self.assertIsNotNone(result)
        copy_instance.setEndPoint.assert_any_call(start_marker, "startToStart")
        copy_instance.setEndPoint.assert_any_call(curr_pos, "endToEnd")
        copy_instance.move.assert_called_with(
            self.cs.textInfos.UNIT_CHARACTER, 1, endPoint="end"
        )

    def test_calculateSelectionRange_backward(self) -> None:
        start_marker = MagicMock()
        curr_pos = MagicMock()

        copy_instance = MagicMock()
        start_marker.copy.return_value = copy_instance

        # Backward cursor movement
        curr_pos.compareEndPoints.return_value = -1
        copy_instance.compareEndPoints.return_value = 1

        result = self.plugin._calculateSelectionRange(start_marker, curr_pos)
        self.assertIsNotNone(result)
        copy_instance.setEndPoint.assert_any_call(curr_pos, "startToStart")
        copy_instance.setEndPoint.assert_any_call(start_marker, "endToEnd")
        copy_instance.move.assert_called_with(
            self.cs.textInfos.UNIT_CHARACTER, 1, endPoint="end"
        )

    def test_calculateSelectionRange_empty_selection(self) -> None:
        start_marker = MagicMock()
        curr_pos = MagicMock()

        copy_instance = MagicMock()
        start_marker.copy.return_value = copy_instance

        # Collapsed selection where start and end points match
        curr_pos.compareEndPoints.return_value = 0
        copy_instance.compareEndPoints.return_value = 0

        result = self.plugin._calculateSelectionRange(start_marker, curr_pos)
        self.assertIsNone(result)

    def test_copy_flow_without_start_marker(self) -> None:
        gesture = MagicMock()
        self.plugin.script_review_copy(gesture)
        self.cs.ui.message.assert_called_with(self.cs._("No start marker set"))


if __name__ == "__main__":
    unittest.main()
