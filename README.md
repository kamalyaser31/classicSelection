# Classic Selection

Classic Selection restores the single-press selection and copying behavior of `NVDA+f9` and `NVDA+f10`.

In modern NVDA, pressing `NVDA+f10` once selects the text between the start marker and review cursor, requiring a second press within a short time window to actually copy the text to the clipboard. This add-on restores the classic, faster behavior: one press on `NVDA+f9` marks the start, and one single press on `NVDA+f10` immediately copies the review selection to your clipboard.

## Problems it solves

- Eliminates the need to double-press `NVDA+f10` to copy text from the review cursor.
- Copies text directly without altering or disrupting the application's native selection or system caret.
- Supports both forward and backward review cursor movement relative to the start marker.
- Fully integrates with NVDA's Input Gestures dialog so you can remap or review shortcuts.

## How to use it

1. Move your review cursor to where you want copying to begin.
2. Press `NVDA+f9`. NVDA announces "Start marked".
3. Move your review cursor forward or backward (by character, word, or line) to where you want copying to end.
4. Press `NVDA+f10` once. NVDA copies the text and announces "Review selection copied to clipboard".

No extra setup or configuration is required.

## Compatibility

- **Minimum NVDA Version:** 2024.1
- **Last Tested NVDA Version:** 2026.2
- Supports both 32-bit and 64-bit Python runtimes (Python 3.11 and Python 3.13).

## Installation

1. Download the latest `classicSelection-2026.1.nvda-addon` file from the [Releases page](https://github.com/kamalyaser31/classicSelection/releases).
2. Open the downloaded file with NVDA.
3. Confirm the installation prompt and restart NVDA.

## Reporting issues

If you encounter any problem:

1. Open the NVDA Log Viewer by pressing `NVDA+f1`.
2. Look for any log lines beginning with `ClassicSelection`.
3. Copy the relevant log lines and submit an issue on the [Issues page](https://github.com/kamalyaser31/classicSelection/issues). The log lines contain no personal data and are safe to share publicly.

## For developers

The add-on is structured using NVDA's official SCons add-on template. To run the automated tests, run `python run_tests.py` from the project root. To build the add-on package, run `scons`.

## Developer

- **Developer:** Kamal Yaser
- **Email:** [kamalyaser31@gmail.com](mailto:kamalyaser31@gmail.com)
- **Telegram:** [@kamalyaser31](https://t.me/kamalyaser31)
- **Original Author:** Tyler Spivey <tspivey@pcdesk.net>

## License

This add-on is released under the GNU General Public License, version 2 (GPL v2).
