# User Parameters Floating Palette — Fusion 360 Add-in

A floating, always-accessible palette for viewing, editing, creating, and deleting **user parameters** in Autodesk Fusion 360.

**This is a fork** of the original [ParamEdit](https://github.com/tapnair/ParamEdit) by Patrick Rainsberry (tapnair).

I created this version because I wanted a few missing functions (inline create/delete + a persistent floating window) so I could stay inside the add-in the whole time instead of constantly going back and forth between the model and the standard User Parameters menu/popup.

## Features

- Floating/resizable palette (dock it or leave it floating)
- View + edit user parameter expressions directly
- Auto-apply on Enter or when you click out of a field
- Create new parameters (name, expression/value, unit, comment)
- Delete parameters with a red X (with confirmation)
- Batch Apply button
- Refresh button
- Works with text and numeric parameters

## Requirements

- Autodesk Fusion 360
- An open **parametric design** (you must be in the Model / Design workspace)

## Installation in Fusion 360

### Recommended: Add Existing Add-in (no copy needed)

1. Download or `git clone` this repository.
2. In Fusion 360 go to the **Utilities** tab (or **Tools** menu) → **Scripts and Add-Ins**.
3. Switch to the **Add-Ins** tab.
4. Click the green **+** button ("Add existing script or add-in").
5. Browse to the `UserParamWindow` folder and select it.
6. In the list, select **UserParamWindow** and click **Run**.
7. (Optional but recommended) Check **Run on Startup** so it loads automatically.

### Manual installation (copy to AddIns folder)

Copy the entire `UserParamWindow` folder to your Fusion Add-Ins directory:

| Platform | Destination |
|----------|-------------|
| Windows  | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\UserParamWindow` |
| macOS    | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/UserParamWindow` |

Then restart Fusion 360 and enable it from **Scripts and Add-Ins**.

After installation the command appears under:
- **Solid → Modify** panel
- Utilities / main toolbar (depending on your workspace)

## Usage

1. Open a parametric design.
2. Click **User Parameters** button.
3. The palette opens as a floating window.
4. Edit expressions — they apply automatically on Enter or blur.
5. Use the **+ Add** area at the bottom to create new parameters.
6. Click the red **X** at the end of a row to delete (with confirmation).
7. Use the refresh icon (top right) if the list gets out of sync.

The palette remembers its position and size between uses.

## Project Structure

```
UserParamWindow/                 # The actual add-in you install
├── UserParamWindow.py
├── UserParamWindow.manifest
├── UserParamWindowCommand.py
├── palette.html
├── Fusion360Utilities/
└── resources/

README.md
KNOWN_ISSUES.md
.gitignore
```

(The original modal ParamEdit files have been removed to keep the repo focused on the floating palette version.)

## Known Issues

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Credits & Fork Info

- Forked from [ParamEdit](https://github.com/tapnair/ParamEdit) by Patrick Rainsberry
- Palette UI pattern inspired by [Fusion360AddinSkeleton](https://github.com/tapnair/Fusion360AddinSkeleton)
- This fork adds the floating palette + create/delete functionality so you don't have to leave the window to manage parameters.

## License

Licensed under the MIT License (same as upstream). See upstream repository for full license text.