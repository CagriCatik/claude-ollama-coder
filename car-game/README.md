# Three.js Car Game

A tiny 3‑D car game built with the Three.js library.

## How to Run
1. Install a static web server (e.g., `python -m http.server` or `npx serve`).
2. Point the server at the project root and open the URL in a browser.
   ```sh
   # Example with Python 3
   python -m http.server 8000
   ```
3. The game automatically starts. Use **W/A/S/D** or the arrow keys to accelerate and steer.

## Game Controls
- **W / Arrow Up** – accelerate forward
- **S / Arrow Down** – accelerate backward (reverse)
- **A / Arrow Left** – steer left
- **D / Arrow Right** – steer right
- **Right‑mouse button + drag** – rotate camera
- **Shift + right‑mouse drag** – zoom in/out
- **Right‑mouse + middle‑mouse** – pan (move horizon)

## Customizing
- **Obstacles** – edit `assets/level.json` to add more boxes.
- **Vehicle model** – replace the default box geometry in `src/Vehicle.js` with a loaded GLTF/OBJ model.

Enjoy!
