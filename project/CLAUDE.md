# instructions.md

## Project goal

Build a modern, interactive webpage using **Three.js**.  
The page should render a 3D scene in the browser and feel polished, performant, and easy to maintain.

## General requirements

- Use **plain JavaScript** unless the task explicitly asks for TypeScript.
- Use **Three.js** as the main 3D library.
- Keep the code modular and readable.
- Prefer simple architecture over clever nonsense.
- Do not introduce heavy dependencies unless clearly justified.
- The result must run locally in a browser with minimal setup.

## Output expectations

When making changes, always:

1. Explain the plan briefly.
2. Create or update the necessary files.
3. Keep file structure clean and minimal.
4. Ensure the final result is runnable.
5. Summarize what was changed and how to run it.

## Preferred project structure

Use a structure like this unless the project already has a better one:

```text
/project-root
  index.html
  style.css
  main.js
  /assets
````

If the project becomes more complex, use:

```text
/project-root
  index.html
  /src
    main.js
    scene.js
    lights.js
    objects.js
    controls.js
  /assets
  style.css
```

## HTML requirements

- Create a minimal `index.html`.
- Mount the Three.js renderer into the page body or a dedicated container.
- Include useful meta tags:

  - charset
  - viewport
  - title
- Do not clutter HTML with unnecessary wrappers.

## CSS requirements

- Remove default body margin.
- Make the canvas fill the viewport unless instructed otherwise.
- Use clean, modern styling for overlays or UI.
- If there is text on top of the canvas, ensure readability and proper layering.
- Avoid bloated CSS frameworks unless requested.

## Three.js requirements

Always include these basics:

- `Scene`
- `PerspectiveCamera`
- `WebGLRenderer`
- at least one visible mesh
- lighting suitable for the materials in use
- responsive resize handling
- animation loop using `requestAnimationFrame`

## Scene defaults

Unless told otherwise, use sensible defaults:

- Background color: dark neutral tone
- Camera: positioned so the main object is clearly visible
- Geometry: start with a cube, sphere, torus knot, or similarly simple object
- Materials: use `MeshStandardMaterial` unless a different material is needed
- Lighting:

  - ambient light
  - directional light or point light

## Interaction

If interaction is appropriate, prefer:

- mouse-driven orbit controls
- subtle hover or rotation animations
- smooth transitions

If using OrbitControls:

- keep damping enabled
- prevent chaotic movement
- avoid absurd zoom ranges

## Performance rules

- Keep geometry and effects lightweight unless the task explicitly asks for high complexity.
- Be careful with particle counts, shadows, and postprocessing.
- Use device pixel ratio carefully:

  - `Math.min(window.devicePixelRatio, 2)`
- Dispose of Three.js resources when needed.
- Do not create memory leaks through repeated object creation inside the render loop.

## Code quality rules

- Write clear variable and function names.
- Keep setup code separated from animation/update logic.
- Add comments only where they genuinely help.
- Avoid giant monolithic files once complexity grows.
- Do not hardcode magic values everywhere; group tunable settings when useful.

## Responsiveness

The scene must adapt to window resizing:

- update camera aspect
- call `camera.updateProjectionMatrix()`
- update renderer size
- update pixel ratio appropriately

## Debugging and reliability

When something is broken:

- identify the likely cause clearly
- fix the root issue, not just the symptom
- avoid guessing blindly
- preserve working code where possible

Common things to check:

- incorrect import paths
- missing renderer append
- camera facing wrong direction
- object outside view frustum
- lack of lighting with non-basic materials
- resize handling issues
- module loading problems

## Visual style guidance

Default visual direction:

- modern
- minimal
- smooth
- cinematic but restrained

Avoid:

- random flashy effects with no purpose
- clashing colors
- overwhelming UI
- fake sophistication glued together with spaghetti code

## When asked to enhance the page

Possible improvements Claude may add when relevant:

- better lighting
- shadows
- environment-like background colors or gradients
- floating animation
- interactive camera controls
- loading external models
- simple postprocessing
- HUD text or buttons
- scroll-driven animation

Only add these if they fit the request.

## If external assets are needed

- Prefer lightweight public-domain or user-provided assets.
- Clearly state where assets should be placed.
- Do not assume unavailable files exist.
- If using a GLTF model or texture, include the expected path in code and mention it in the summary.

## If using modules

Prefer modern ES module imports.

Example approach:

- use a bundler like Vite if setup is allowed
- otherwise use browser-compatible module imports when appropriate

If creating a fresh project, Vite is a good default.

## Fresh project preference

If starting from scratch, prefer this stack:

- Vite
- JavaScript
- Three.js

## Example baseline behavior

If no special creative direction is provided, build:

- a full-screen webpage
- one animated 3D object
- ambient and directional light
- orbit controls
- responsive resizing
- a small title overlay in the corner

## Response style

When helping with this project:

- be practical
- be precise
- do not overexplain trivial things
- do not invent requirements
- do not pretend code works if it has not been made coherent

## Definition of done

A task is done when:

- the code is complete
- the browser page renders correctly
- the scene is visible
- resizing works
- the result matches the request
- the file structure is understandable
- run instructions are included if setup is required
