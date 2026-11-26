# World clocks for Fenn

Times in other cities on your Fenn notch.

## What it does

- Wide tile: the first two cities and their current time.
- Page: your local time plus every city you added, each with its offset and Today/Tomorrow/Yesterday.
- Add a city by name (`Tokyo`, `new york`) or by zone (`Asia/Dubai`). Click the x to remove one.
- Defaults: London, New York, Tokyo, Sydney. Updates once a minute.
- A **24-hour** switch changes the clocks to 12-hour (`9:12 PM`).
- If the time zone data is missing, the page shows an **Install tzdata** button that fixes it in one click.

## Install

1. Copy this folder to `%APPDATA%\Fenn\plugins\worldclock\` so that `plugin.toml` and `main.py` sit directly inside it.
2. In Fenn, open **Settings** and turn on **Plugin dev mode**. The tile appears within a few seconds, with no restart. (Without dev mode, restart Fenn.)
3. New tiles are added after the built-in ones, possibly on the second page. Use the pencil in the grid to move or resize it.

Requires Fenn with plugin support.

## Requirements

Python 3.9+ (Fenn can set it up for you, or use your own). Windows has no timezone database of its own, so the clocks need the `tzdata` package. If it is missing, cities show `?` and the page offers an **Install tzdata** button. You can also run `python -m pip install tzdata` yourself, in the Python that runs the plugin.

## Network and privacy

- Normally none. Everything is computed on your PC.
- **Only if you press Install tzdata:** the plugin runs `python -m pip install tzdata` with the Python that runs it, which downloads that package from pypi.org. Nothing else ever runs pip, and the package name is fixed in the code.

## Settings and data

- Your city list and the 12/24-hour choice are saved in `%APPDATA%\Fenn\plugin-data\worldclock\config.json`.

## Limitations

- A name that matches several zones uses the first match alphabetically. Type the full zone (`America/Chicago`) to be exact.

## Troubleshooting

- **Tile says "Stopped":** hover it to see the error and the last lines of the plugin's output.
- **Nothing happens:** Fenn can set up Python for you. If that didn't work, make sure `python --version` works in a new PowerShell window, or install Python from python.org and tick "Add python.exe to PATH".
- **Full log:** the logs of the last ten Fenn runs are in `%APPDATA%\Fenn\logs`.
- **Plugins are programs.** They run with the same rights as Fenn. Read the code (it is one short file) before installing any plugin.

## Credits and license

MIT. See `LICENSE`.

## Files

- `plugin.toml`: the plugin manifest.
- `main.py`: the whole plugin.
- `LICENSE`, `.gitignore`.
