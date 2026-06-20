# Known issues

## Palette may not load correctly on first run

**Symptom:** The palette opens but stays on "Loading…", shows wrong size, or does not list parameters until you click **Refresh** (or restart Fusion).

**Likely cause:** Fusion’s HTML palette webview sometimes is not ready when the add-in first sends data, especially right after the add-in is enabled or on the very first open in a session.

**Workarounds:**

1. Click the **refresh** icon (circular arrow, top-right of the palette).
2. Close and reopen the palette via **User Parameters** in the toolbar.
3. In **Scripts and Add-Ins**, stop and start the **UserParamWindow** add-in.
4. Restart Fusion 360 (often clears webview/palette state for the session).

**Status:** Fixed.

The fix involved:
- Creating the palette visible from the `add()` call.
- Multiple explicit `palette.height = PALETTE_HEIGHT` forces from Python right after `isVisible`, after pushing content, and (with a small nudge) when the JS signals `'paletteReady'`.
- `_commit_palette_content_height` now always targets at least the designed size when the client requests a layout commit.
- JS side fires a large fixed-size `commitPaletteSize` request as soon as `window.adsk` is available (plus measured kicks after render).

First open now shows the full palette immediately. No more minimize/restore dance required.

---



## Vertical resize can snap back slightly on mouse-up

**Symptom:** While dragging to resize the palette taller it looks correct, but on release the window may shrink a bit.

**Workaround:** Resize again or drag slightly taller than needed; the UI tries to commit the larger height after resize ends.

**Status:** Mitigated in current builds; report if it still happens on your Fusion version.