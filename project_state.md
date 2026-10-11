# Project State: classicSelection

## Overview
- **Name:** classicSelection
- **Type:** NVDA Add-on (Global Plugin)
- **Version:** 2026.1
- **Original Author:** Tyler Spivey <tspivey@pcdesk.net>
- **Target NVDA Versions:** Minimum 2024.1.0, Last Tested 2026.2.0

## Architecture & Implementation
- **Layout:** Standard NVDA AddonTemplate SCons layout (`site_scons/`, `sconstruct`, `buildVars.py`, `addon/`).
- **Build Artifact:** `classicSelection-2026.1.nvda-addon` (compiled translation, generated manifests, HTML docs).
- **Core Plugin:** `addon/globalPlugins/classicSelection.py` implements a `GlobalPlugin` inheriting from `globalPluginHandler.GlobalPlugin`.
- **Architecture:** Clean Code decomposition with extracted `_calculateSelectionRange`, dedicated `_syncCoreStartMarker`/`_clearCoreStartMarker` helpers with targeted exception handling, and full `terminate()` lifecycle cleanup.
- **Scripts:**
  - `script_review_markStartForCopy` (`NVDA+f9`): Marks review cursor start position and synchronizes with `globalCommands.commands._reviewCopyStartMarker`.
  - `script_review_copy` (`NVDA+f10`): Directly copies text between start marker and current review cursor position to clipboard on single press (both forward and backward movement supported).
- **Standards & Verification:** Python 3.11/3.13 64-bit compatible, PEP 8, formatted with `black`, linted with `ruff` and `flake8` (max-line-length 88), 5/5 unit tests passing via `run_tests.py`.
