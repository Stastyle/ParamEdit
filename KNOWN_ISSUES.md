# Known issues

## Palette may not load correctly on first run

**Symptom:** The palette opens but stays on "Loading…", shows wrong size, or does not list parameters until you click **Refresh** (or restart Fusion).

**Likely cause:** Fusion’s HTML palette webview sometimes is not ready when the add-in first sends data, especially right after the add-in is enabled or on the very first open in a session.

**Workarounds:**

1. Click the **refresh** icon (circular arrow, top-right of the palette).
2. Close and reopen the palette via **User Parameters** in the toolbar.
3. In **Scripts and Add-Ins**, stop and start the **UserParamWindow** add-in.
4. Restart Fusion 360 (often clears webview/palette state for the session).

**Status:** Under investigation. A full Fusion restart may resolve it; if it persists after restart, use Refresh until a code-side fix is added.

---

## Vertical resize can snap back slightly on mouse-up

**Symptom:** While dragging to resize the palette taller it looks correct, but on release the window may shrink a bit.

**Workaround:** Resize again or drag slightly taller than needed; the UI tries to commit the larger height after resize ends.

**Status:** Mitigated in current builds; report if it still happens on your Fusion version.