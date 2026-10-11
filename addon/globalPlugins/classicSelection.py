# Copyright 2016 Tyler Spivey <tspivey@pcdesk.net>
# Updated for modern NVDA (2024.1 - 2026.x)
# See the license in copying.txt.

from __future__ import annotations

import addonHandler
import api
import globalPluginHandler
import inputCore
from logHandler import log
from scriptHandler import script
import textInfos
import ui

try:
    from comtypes import COMError
except ImportError:
    COMError = type("COMError", (Exception,), {})

try:
    import globalCommands
except ImportError:
    globalCommands = None

addonHandler.initTranslation()

try:
    _
except NameError:
    from gettext import gettext as _

# Translators: Category for Classic Selection in Input Gestures dialog.
SCRCAT_CLASSICSELECTION = _("Classic Selection")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = SCRCAT_CLASSICSELECTION

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._copyStartMarker: textInfos.TextInfo | None = None
        self._copyStartMarkerObj = None

    def terminate(self) -> None:
        self._copyStartMarker = None
        self._copyStartMarkerObj = None
        self._clearCoreStartMarker()
        super().terminate()

    def _syncCoreStartMarker(self, reviewPos: textInfos.TextInfo) -> None:
        """Synchronize the review start marker with NVDA core commands."""
        if globalCommands and hasattr(globalCommands, "commands"):
            try:
                globalCommands.commands._reviewCopyStartMarker = reviewPos.copy()
                globalCommands.commands._reviewCopyStartMarkerObj = reviewPos.obj
                globalCommands.commands._reviewSelectThenCopyRange = None
            except (AttributeError, RuntimeError) as e:
                log.debug(f"ClassicSelection: failed to sync marker with core: {e}")

    def _clearCoreStartMarker(self) -> None:
        """Clear review start markers in NVDA core commands."""
        if globalCommands and hasattr(globalCommands, "commands"):
            try:
                globalCommands.commands._clearReviewCopyStartMarker()
            except (AttributeError, RuntimeError) as e:
                log.debug(f"ClassicSelection: failed to clear marker in core: {e}")

    def _calculateSelectionRange(
        self,
        startMarker: textInfos.TextInfo,
        currentPos: textInfos.TextInfo,
    ) -> textInfos.TextInfo | None:
        """Create a selection range between startMarker and currentPos
        matching core semantics.
        """
        copyMarker = startMarker.copy()
        try:
            # Support both forward and backward review cursor movement
            if currentPos.compareEndPoints(startMarker, "endToEnd") > 0:
                copyMarker.setEndPoint(startMarker, "startToStart")
                copyMarker.setEndPoint(currentPos, "endToEnd")
                copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
            else:
                copyMarker.setEndPoint(currentPos, "startToStart")
                copyMarker.setEndPoint(startMarker, "endToEnd")
                copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
        except (COMError, LookupError, NotImplementedError, RuntimeError) as e:
            log.debug(f"ClassicSelection: error comparing endpoints: {e}")
            return None

        if copyMarker.compareEndPoints(copyMarker, "startToEnd") == 0:
            return None

        return copyMarker

    @script(
        # Translators: Input help message for mark review position command.
        description=_(
            "Marks the current position of the review cursor as the start "
            "of text to be copied"
        ),
        category=SCRCAT_CLASSICSELECTION,
        gestures=["kb:NVDA+f9"],
    )
    def script_review_markStartForCopy(self, gesture: inputCore.InputGesture) -> None:
        reviewPos = api.getReviewPosition()
        if not reviewPos:
            # Translators: Presented when there is no text to review or copy.
            ui.message(_("No text to copy"))
            return

        self._copyStartMarker = reviewPos.copy()
        self._copyStartMarkerObj = reviewPos.obj
        self._syncCoreStartMarker(reviewPos)

        # Translators: Indicates start of review cursor text to be copied.
        ui.message(_("Start marked"))

    @script(
        # Translators: Input help message for copy selected review cursor text.
        description=_(
            "Retrieves the text from the previously set start marker up to "
            "and including the current position of the review cursor and "
            "copies it to the clipboard"
        ),
        category=SCRCAT_CLASSICSELECTION,
        gestures=["kb:NVDA+f10"],
    )
    def script_review_copy(self, gesture: inputCore.InputGesture) -> None:
        if not self._copyStartMarker:
            # Translators: Presented when attempting copy without start marker.
            ui.message(_("No start marker set"))
            return

        reviewPos = api.getReviewPosition()
        if not reviewPos:
            ui.message(_("No text to copy"))
            return

        currentPos = reviewPos.copy()
        if (
            self._copyStartMarkerObj != currentPos.obj
            or currentPos.__class__ is not self._copyStartMarker.__class__
        ):
            # Translators: Presented when trying to copy across different objects.
            ui.message(_("The start marker must reside within the same object"))
            return

        copyMarker = self._calculateSelectionRange(self._copyStartMarker, currentPos)
        if not copyMarker:
            ui.message(_("No text to copy"))
            return

        if copyMarker.copyToClipboard():
            # Translators: Presented when review text is copied to clipboard.
            ui.message(_("Review selection copied to clipboard"))
        else:
            ui.message(_("No text to copy"))
            return

        self._copyStartMarker = None
        self._copyStartMarkerObj = None
        self._clearCoreStartMarker()
