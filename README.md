# UserParamWindow

Fusion 360 add-in that shows **user parameters** in a **floating palette** inside Fusion. Forked from [tapnair/ParamEdit](https://github.com/tapnair/ParamEdit) and extended with palette UI, create/delete parameters, and auto-apply on edit.

## Features

- Floating, resizable palette (not a modal dialog)
- View and edit user parameter expressions
- Auto-apply when you press **Enter** or click outside an expression field
- Create new user parameters (name, value, unit, comment)
- Delete deletable parameters
- Manual **Apply** for batch edits
- Refresh button (icon, top-right) to reload from the design

## Requirements

- Autodesk Fusion 360 (Windows or Mac)
- An open **parametric design** (Model workspace)

## Installation

### Option A — project folder (development)

1. Clone or copy this repository.
2. In Fusion: **Utilities → Scripts and Add-Ins → Add-Ins** (green **+**).
3. Add the `UserParamWindow` folder from this repo (the folder that contains `UserParamWindow.py` and `UserParamWindow.manifest`).
4. Select **UserParamWindow**, click **Run**.

### Option B — Fusion Add-Ins directory

Copy the `UserParamWindow` folder to your Fusion add-ins location, then run it from **Scripts and Add-Ins**:

| OS | Path |
|----|------|
| Windows | `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| Mac | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

See [tapnair installation guide](https://tapnair.github.io/installation.html) for details.

## Usage

1. Open a design with user parameters (or add new ones in the palette).
2. In the **Solid → Modify** panel, click **User Parameters**.
3. Edit expressions in the table; changes apply on **Enter** or when the field loses focus.
4. Use the **+ Add** section at the bottom to create parameters.
5. Use the refresh icon (top-right) if the list needs reloading.

## Project layout

```
UserParamWindow/
├── UserParamWindow.py           # Add-in entry (run/stop)
├── UserParamWindow.manifest
├── UserParamWindowCommand.py    # Palette + parameter CRUD
├── palette.html                 # Floating UI
├── Fusion360Utilities/          # Shared utilities (from ParamEdit fork)
└── resources/                   # Toolbar icons
```

## Known issues

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Credits

- Based on [ParamEdit](https://github.com/tapnair/ParamEdit) by Patrick Rainsberry (tapnair)
- Palette pattern inspired by [Fusion360AddinSkeleton](https://github.com/tapnair/Fusion360AddinSkeleton)

## License

Same lineage as ParamEdit; refer to upstream repository for license terms.