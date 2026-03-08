# Three.js Interactive Demo

A small, self‑contained web page that renders a 3D scene using **Three.js**.
Features include:

- A rotating cube and torus‑knot
- Ambient, directional, and hemisphere lighting
- Ground plane for visual reference
- OrbitControls with damping and sensible zoom limits
- UI overlay with **Reset Camera** and **Toggle Auto‑Rotate** buttons
- Responsive resizing handling
- No build tools – everything loads from a CDN

---

## Project Structure

```shell
project/
├─ index.html      # HTML entry point with import‑map
├─ style.css        # Simple CSS for full‑screen canvas + UI overlay
├─ main.js          # Three.js scene setup and animation loop
└─ CLAUDE.md        # Project guidelines (not needed at runtime)
```

---

## Getting Started

Because the page uses ES‑module imports, it must be served over HTTP rather than opened directly from the file system.

### 1. Clone / download the repo

```shell
git clone <repo‑url>
cd project
```

### 2. Serve the folder

You can use any static‑file server. Below are a few quick options:

| Tool | Command |
|------|---------|
| **Python 3** | `python -m http.server 8000` |
| **Node (http‑server)** | `npx http-server -p 8000` |
| **VS Code Live Server** | Open the folder in VS Code → *Live Server* extension → *Go Live* |
| **Docker** | `docker run -v "$(pwd)":/usr/share/nginx/html:ro -p 8080:80 nginx` |

The server will expose the files at `http://localhost:8000` (or whichever port you choose).

### 3. Open the demo

Navigate to the served URL in a modern browser (Chrome, Edge, Firefox, Safari).

```shell
http://localhost:8000/index.html
```

You should see a dark gradient background with a rotating cube and torus‑knot. Use the mouse to orbit, pan, and zoom. Click **Reset Camera** to restore the default view, or **Toggle Auto‑Rotate** to pause the animation.

---

## Development & Customisation

- **Adding objects** – edit `main.js` and create new geometries / meshes.
- **Changing colors** – modify the `color` values in the material definitions.
- **Lighting tweaks** – adjust the intensity or position of the existing lights, or add new light types.
- **Styling** – update `style.css` for UI overlay tweaks or background changes.

Because all assets are loaded from a CDN, no `npm install` or bundler configuration is required. If you later decide to move to a bundler (e.g., Vite) you can replace the import‑map with a local import.

---

## Browser Compatibility

- ES‑module support (modern browsers)
- WebGL 2 (most current desktop and mobile browsers)

If the page does not render, ensure your browser is up to date and that hardware acceleration is enabled.

---

## License & Credits

- **Three.js** – MIT License (loaded from CDN)
- **Demo code** – written for this repository; feel free to reuse or modify.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|---------------|-----|
| Blank page, console errors about “`import`” | Opening file via `file://` instead of a server | Serve the directory over HTTP (see step 2). |
| No geometry visible | Camera positioned incorrectly or objects behind camera | Use the **Reset Camera** button or check `camera.position` in `main.js`. |
| Controls feel jittery | `devicePixelRatio` not clamped, high‑dpi screen | The code already caps pixel ratio at `2`. If you modified it, restore the limit. |

---

**Enjoy exploring Three.js!** 🎉