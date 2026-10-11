from site_scons.site_tools.NVDATool.typings import (
    AddonInfo,
    BrailleTables,
    SymbolDictionaries,
)
from site_scons.site_tools.NVDATool.utils import _

addon_info = AddonInfo(
    addon_name="classicSelection",
    addon_summary=_("Classic Selection"),
    addon_description=_(
        """Restores the classic review cursor selection and copy behaviour of NVDA+f9 and NVDA+f10. Press NVDA+f9 to mark the start, and NVDA+f10 once to directly copy the review selection to the clipboard."""
    ),
    addon_version="2026.1",
    addon_changelog=_(
        """- Version 2026.1: Modernized for NVDA 2024.1 through 2026.2 with 64-bit support, single-press review cursor copying, bi-directional review selection, and full input gesture integration."""
    ),
    addon_author="Tyler Spivey <tspivey@pcdesk.net>, Kamal Yaser <kamalyaser31@gmail.com>",
    addon_url="https://github.com/kamalyaser31/classicSelection",
    addon_sourceURL="https://github.com/kamalyaser31/classicSelection",
    addon_docFileName="readme.html",
    addon_minimumNVDAVersion="2024.1.0",
    addon_lastTestedNVDAVersion="2026.2.0",
    addon_updateChannel=None,
    addon_license="GPL v2",
    addon_licenseURL="https://www.gnu.org/licenses/gpl-2.0.html",
)

pythonSources = ["addon/**/*.py"]
i18nSources: list[str] = pythonSources + ["buildVars.py"]
excludedFiles: list[str] = ["*.pyc"]
baseLanguage: str = "en"
markdownExtensions: list[str] = []
brailleTables: BrailleTables = {}
symbolDictionaries: SymbolDictionaries = {}
speechDictionaries: dict = {}
