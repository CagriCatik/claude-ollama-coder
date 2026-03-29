# How to Add Skills to Claude for Your Project

This guide shows you how to configure Claude to help with your Three.js project effectively.

---

## 📋 Option 1: Instructions File (Recommended for VS Code)

### Create `.instructions.md` in Your Project Root

Create a file named `.instructions.md` in the `project/` folder. Claude will automatically use this.

```markdown
# Three.js Development Instructions

## Project Context
This is an interactive Three.js 3D visualization project running in the browser.
- Framework: Three.js
- Language: Plain JavaScript (no TypeScript)
- HTML/CSS/JS structure
- Goals: Performance, modularity, visual polish

## Current Project Files
- `index.html` - Main HTML entry point
- `main.js` - Main 3D scene and animation loop
- `style.css` - Styling for canvas and UI
- `CLAUDE.md` - Project guidelines

## Your Capabilities for This Project

### File Operations
You can:
- Read any JavaScript/HTML/CSS file in this project
- Create new files
- Modify existing files
- Provide code with explanations

### Three.js Skills
Help with:
1. **Scene Setup**: Cameras, renderers, scenes, geometries, materials
2. **Geometry**: Shapes, custom geometries, buffer geometries
3. **Materials**: Standard, Lambert, Phong, normal maps
4. **Lighting**: Ambient, directional, point, spotlights
5. **Animation**: requestAnimationFrame loops, tweens, transformations
6. **Interaction**: Mouse/touch controls, raycasting, events
7. **Performance**: Optimization, culling, LOD techniques
8. **Responsive**: Canvas resize handling, mobile compatibility

### Best Practices
- Keep code modular and readable
- Prefer MeshStandardMaterial for modern look
- Use OrbitControls for interactive scenes
- Handle window resize events
- Implement proper lighting for materials
- Test on different screen sizes

## How to Request Help

### For Scene Building
"I need a rotating cube with lighting. Here are the current file contents: [show files]"

### For Debugging
"My geometry isn't showing. Here's my code: [paste]. What's wrong?"

### For Features
"Add interactive mouse controls using raycasting to let users click objects."

### For Optimization
"My scene is slow with 10,000 objects. How should I optimize?"

## Output Format
Always provide:
1. Brief explanation of the plan
2. Complete code changes
3. How to run/test
4. What was changed and why

## When to Ask
- Architecture/design decisions
- Performance optimization
- Debugging rendering issues
- Best practices for 3D interactions
- Code refactoring
```

### How Claude Automatically Uses This
When you open your project folder in VS Code and chat with Claude, it will:
1. Automatically read `.instructions.md`
2. Use those guidelines for all responses
3. Remember your project context
4. Provide more relevant help

---

## 🛠️ Option 2: Custom Tools/Skills File

Create `project/.claude/skills.json` to define tools Claude can use:

```json
{
  "skills": [
    {
      "name": "read_project_file",
      "description": "Read any file in the project",
      "enabled": true
    },
    {
      "name": "create_component",
      "description": "Create a new JavaScript Three.js component",
      "parameters": {
        "name": "Component name (e.g., 'lights', 'geometry')",
        "type": "string"
      }
    },
    {
      "name": "test_in_browser",
      "description": "Test current code in browser",
      "enabled": true
    }
  ],
  "context_files": [
    "CLAUDE.md",
    "README.md",
    "main.js"
  ]
}
```

---

## 🎯 Option 3: Copilot Instructions (VS Code Copilot)

If using GitHub Copilot Chat in VS Code, create `.copilot-instructions` file:

```
# Three.js Project Context

## When helping with this project:

1. **Always show working code**
   - Complete, runnable examples
   - Include necessary imports
   - Add comments for complex parts

2. **For Three.js specifically**
   - Use MeshStandardMaterial as default
   - Always include proper lighting
   - Handle responsive resizing
   - Test on both desktop and mobile viewport sizes

3. **Code structure**
   - Keep related code together
   - Separate concerns (scene, lights, objects, interaction)
   - Use clear function names
   - Add JSDoc comments for main functions

4. **Performance matters**
   - Watch for memory leaks
   - Dispose geometries and materials when removing objects
   - Use efficient rendering patterns
   - Consider using BufferGeometry for large meshes

5. **When I ask for changes**
   - Show diff of what changed
   - Explain why the change helps
   - Show how to test it
   - Ask if you should split into separate files as project grows
```

---

## 📝 Option 4: Simple Knowledge File

Create `project/.claude/context.md` with your project knowledge:

```markdown
# Three.js Project Knowledge Base

## Current State
- Basic Three.js scene with canvas
- Responsive to window resize
- Uses requestAnimationFrame for animation loop

## Typical Patterns in This Project

### Material Setup
```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0x4488ff,
  metalness: 0.7,
  roughness: 0.3
});
```

### Light Setup
```javascript
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 10, 7);
scene.add(ambientLight, directionalLight);
```

### Animation Loop
```javascript
function animate() {
  requestAnimationFrame(animate);
  // Update objects
  mesh.rotation.x += 0.01;
  renderer.render(scene, camera);
}
animate();
```

### Resize Handler
```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Common Tasks

### Add Interaction
Use Raycaster for mouse picking, OrbitControls for camera movement

### Add Animation
Use TWEEN.js or custom animation within requestAnimationFrame

### Optimize Performance
- Dispose materials/geometries when unneeded
- Use LOD for distant objects
- Batch render calls
- Use BufferGeometry
```

---

## 🚀 Step-by-Step Setup

### 1. Create Instructions File
```bash
cd project
echo "# Three.js Development Instructions" > .instructions.md
# Then add content from Option 1 above
```

### 2. Update Project Structure (Optional)
If your project grows, organize like this:
```
project/
├── index.html
├── style.css
├── src/
│   ├── main.js           (entry point)
│   ├── scene.js          (scene setup)
│   ├── lights.js         (lighting)
│   ├── geometry.js       (objects)
│   ├── materials.js      (materials)
│   └── interaction.js    (mouse/touch)
├── .instructions.md      (tells Claude how to help)
└── .claude/
    └── settings.local.json
```

### 3. Tell Claude About It
Share your project structure:
```
I have a Three.js project with:
- Main scene in main.js
- Custom geometries in src/geometry.js
- Lighting setup in src/lights.js
- OrbitControls for interaction

Here's what I need help with: [your request]
```

---

## 💬 Smart Ways to Ask for Help

### ❌ Vague
```
"Help me build a 3D scene"
```

### ✅ Specific
```
"I need a rotating cube with:
- Shiny gold material
- Proper lighting to show the material
- Subtle rotation animation
Here's my current main.js: [paste]"
```

### ❌ Unclear
```
"Why doesn't my code work?"
```

### ✅ Clear
```
"My sphere isn't visible. I created it with:
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

The canvas shows black. What's missing?"
```

### ❌ Generic
```
"Optimize my Three.js scene"
```

### ✅ Specific
```
"My scene with 5,000 particles is running at 10fps. 
Each particle is a separate THREE.Mesh.
How should I combine them for better performance?"
```

---

## 🎓 Examples: Requesting Help

### Example 1: Add Feature
```
I want to add mouse interaction so users can pick objects and drag them.
My current scene has 3 cubes positioned at different locations.
Here's my main.js: [paste]
```

### Example 2: Debug
```
Error: "Cannot read property 'geometry' of undefined"
This happens when I try to rotate objects.
Here's the relevant code: [paste]
What's wrong?
```

### Example 3: Improve
```
I have a simple rotating cube. Now I want:
1. Add 3 different colored rotating cubes
2. Add interactive controls (mouse to rotate camera)
3. Add smooth shadows

Here's current code: [paste]
```

### Example 4: Performance
```
My scene with 100 mesh objects runs at 30fps.
The main bottleneck seems to be rendering.
Should I use:
- Merge geometries
- Use InstancedMesh
- Implement LOD (Level of Detail)

Current metrics: [describe]
```

---

## 🔗 Linking Files in Conversation

### In VS Code Copilot Chat
```
Here's my main scene setup: 
[Copy paste the main.js content here]

And my materials file:
[Copy paste materials.js content]

I need to add shadow support.
```

### Pro Tip
Share relevant context:
```
Current state:
- main.js: Basic scene with 1 cube
- style.css: Full viewport canvas
- index.html: Simple bootstrap
- Performance: 60fps with 1 object

Goal: Add 100 interactive particles keeping 60fps
Constraints: No heavy dependencies

Help needed: Architecture for performance
```

---

## ✅ Quick Checklist for Claude Help

Before asking Claude:
- [ ] Describe what you're building
- [ ] Share relevant code (or file names)
- [ ] Show error messages (if any)
- [ ] Explain what you've tried
- [ ] Mention constraints (no external libs, performance, etc.)
- [ ] Share project structure
- [ ] Describe expected outcome

---

## 📚 When to Use Each Option

| Situation | Use This |
|-----------|----------|
| Using VS Code Copilot | `.instructions.md` + `.copilot-instructions` |
| Using claude.ai web | Share your `.instructions.md` content in chat |
| Building complex project | Combine all options + organize into modules |
| Collaborating in team | Add to root `.instructions.md` with team guidelines |
| Long-term project | Maintain updated `.claude/context.md` with patterns |

---

## 🎯 Next Steps

1. **Create `.instructions.md`** in your `project/` folder
2. **Share your current files** with Claude (index.html, main.js, style.css)
3. **Describe your goal** for the Three.js scene
4. **Ask Claude** how to structure or build it

Claude will then have full context to provide better, more specific help! 🚀
