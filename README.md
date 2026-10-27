# Research Stop

A Victoria 3 mod: the game pauses before ahead-of-time research runs past its base cost, so you can switch research before the points go to waste.

**[Subscribe on the Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3828125161)**

![Research Stop](mod/thumbnail.png)

## The problem

A technology from a later era costs 25% more for each unresearched technology from an earlier era in the same category (more if it's two eras back). Researching it early ("ahead of time") is a common trick, but once the earlier technologies arrive (often by technology spread) the cost drops back to the era's base cost. Any progress above that base cost is lost.

For example, Atmospheric Engine (era II, base 10,000) costs 12,500 while one era I production technology is missing. The trick is to research it up to about 9,900, switch to something else, and let it finish when the penalty goes away. If you forget to switch, you waste up to 2,500 innovation.

## What it does

While you research a technology with an ahead-of-time penalty, the mod checks whether next week's progress could pass the base cost. When it could, the game pauses and an alert shows:

- the technology's progress, current cost and base cost
- **Open Technology** to pick something else
- **Keep Researching** to close the alert. It won't stop again for that technology.

The alert closes itself when you switch research. Each technology stops at most once per game session.

Nothing is stored in the save. The mod is GUI-only.

## Compatibility

- Built for Victoria 3 1.13.
- Safe to add to or remove from an existing save.
- Replaces no vanilla files or GUI types. It adds its own widget through `gui/scripted_widgets`, so it works alongside Date Stop and mods that change the tech tree or time controls.
- Text is English only.

## Manual install

Copy the `mod/` folder to `Documents/Paradox Interactive/Victoria 3/mod/Research Stop`. On Linux that's `~/.local/share/Paradox Interactive/Victoria 3/mod/Research Stop`. Then enable it in the launcher.

## How it works

- `gui/scripted_widgets/rsm_widgets.txt` makes the game create the widget in `gui/rsm_research_stop.gui` on startup.
- The widget's data context is the technology being researched. Its base cost is `Technology.GetEra.GetTechnologyCost`. The penalty applies when `Technology.GetCost` is higher than that.
- A `state` with `trigger_when` fires when `progress + GetMaxWeeklyTechnologyProgressForTech` reaches the base cost. The comparisons are done in `int32` via `FixedPointToInt`: comparing against `IntToFixedPoint(...)` fails at runtime (`FetchData failed`), even though it displays fine. It calls `TimeKeeper.TogglePause` and records the technology's name in the GUI variable system (`rsm_latched`) so it fires once per technology.

## Development

- `mod/` is exactly what ships.
- `tools/install.sh` copies `mod/` into your local mod folder. Run it after each change.
- `python3 tools/make_thumbnail.py` redraws `mod/thumbnail.png`, using the game's EB Garamond font.
- To test: launch with `./victoria3 -debug_mode` from the game's `binaries/` folder (uses the launcher's last playset). Copy `tools/dev/rsm_test.txt` into `mod/events/`, reinstall, start researching Atmospheric Engine as a country with Shaft Mining and a missing era I production technology, then run `event rsm_test.1` and `event rsm_test.2` in the console. Progress goes to 9,950 and the stop triggers. Remove the file again before uploading.
- No `script_docs` dump was needed: GUI data-function signatures (e.g. `CDataEra::GetTechnologyCost` returns `int`) were read from `CallFunction<...>` strings in the game binary.
