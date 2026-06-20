# UserParamWindow (ParamEdit fork)

Fusion 360 add-in that shows **user parameters** in a **floating palette** inside Fusion. This repository is a fork of [tapnair/ParamEdit](https://github.com/tapnair/ParamEdit). The original modal **ParamEdit** add-in remains at the repo root; the new **UserParamWindow** palette add-in lives in the `UserParamWindow/` folder.

## UserParamWindow features

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

## Installation (UserParamWindow)

### Option A — project folder (development)

1. Clone this repository.
2. In Fusion: **Utilities → Scripts and Add-Ins → Add-Ins** (green **+**).
3. Add the `UserParamWindow` folder (contains `UserParamWindow.py` and `UserParamWindow.manifest`).
4. Select **UserParamWindow**, click **Run**.

### Option B — Fusion Add-Ins directory

Copy the `UserParamWindow` folder to your Fusion add-ins location:

| OS | Path |
|----|------|
| Windows | `%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| Mac | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

See [tapnair installation guide](https://tapnair.github.io/installation.html) for details.

## Usage (UserParamWindow)

1. Open a design with user parameters (or add new ones in the palette).
2. In the **Solid → Modify** panel, click **User Parameters**.
3. Edit expressions in the table; changes apply on **Enter** or when the field loses focus.
4. Use the **+ Add** section at the bottom to create parameters.
5. Use the refresh icon (top-right) if the list needs reloading.

## Project layout

```
UserParamWindow/                 # New floating-palette add-in
├── UserParamWindow.py
├── UserParamWindow.manifest
├── UserParamWindowCommand.py
├── palette.html
├── Fusion360Utilities/
└── resources/

ParamEdit.py                     # Original upstream modal add-in (unchanged)
ParamEditCommand.py
...
```

## Known issues

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

---

## Original ParamEdit (upstream)

The root-level **ParamEdit** add-in is Patrick Rainsberry's original script for editing user parameters in a modal dialog with live preview.

- Install/run **ParamEdit** from the repo root files, or use the upstream [ParamEdit release](https://github.com/tapnair/ParamEdit).
- Usage: **Modify → paramEdit**

## Credits

- Based on [ParamEdit](https://github.com/tapnair/ParamEdit) by Patrick Rainsberry (tapnair)
- Palette pattern inspired by [Fusion360AddinSkeleton](https://github.com/tapnair/Fusion360AddinSkeleton)

## License

Samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). See upstream [LICENSE](LICENSE) where applicable.