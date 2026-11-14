# World clocks for Fenn

Times in other cities on your Fenn notch.

## What it does

- Wide tile: the first two cities and their current time.
- Page: your local time plus every city you added, each with its offset and Today/Tomorrow/Yesterday.
- Add a city by name (`Tokyo`, `new york`) or by zone (`Asia/Dubai`). Click the x to remove one.
- Defaults: London, New York, Tokyo, Sydney. Updates once a minute.

## Install

1. Copy this folder to `%APPDATA%\Fenn\plugins\worldclock\` so that `plugin.toml` and `main.py` sit directly inside it.
2. In Fenn, open **Settings** and turn on **Plugin dev mode**. The tile appears within a few seconds, with no restart. (Without dev mode, restart Fenn.)
3. New tiles are added after the built-in ones, possibly on the second page. Use the pencil in the grid to move or resize it.

Requires Fenn with plugin support.

## Requirements

Python 3.9+ on your PATH. **On Windows run `pip install tzdata` once**: Windows has no timezone database of its own, and without it cities show `?`.

## Network and privacy

- None. Everything is computed on your PC.

## Settings and data

- Your city list is saved in `%APPDATA%\Fenn\plugin-data\worldclock\config.json`.

## Limitations

- A name that matches several zones uses the first match alphabetically. Type the full zone (`America/Chicago`) to be exact.

## Troubleshooting

- **Tile says "Stopped":** hover it to see the error and the last lines of the plugin's output.
- **Nothing happens:** make sure `python --version` works in a new PowerShell window. If it doesn't, install Python from python.org and tick "Add python.exe to PATH".
- **Full log:** The `.log` file in `%APPDATA%\Fenn\` has the plugin's errors.
- **Plugins are programs.** They run with the same rights as Fenn. Read the code (it is one short file) before installing any plugin.

## Credits and license

MIT. See `LICENSE`.

## Files

- `plugin.toml`: the plugin manifest.
- `main.py`: the whole plugin.
- `LICENSE`, `.gitignore`.
