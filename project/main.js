import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

// Camera
const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(3, 2, 4);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lights
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

const directional = new THREE.DirectionalLight(0xffffff, 1);
directional.position.set(5, 10, 7);
scene.add(directional);

const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
scene.add(hemiLight);

// Ground plane
const planeGeometry = new THREE.PlaneGeometry(10, 10);
const planeMaterial = new THREE.MeshBasicMaterial({
  color: 0x222222,
  side: THREE.DoubleSide,
  transparent: true,
  opacity: 0.5
});
const groundPlane = new THREE.Mesh(planeGeometry, planeMaterial);
groundPlane.rotation.x = -Math.PI / 2;
groundPlane.position.y = -1;
scene.add(groundPlane);

// Cube
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00aaff });
const cube = new THREE.Mesh(geometry, material);
cube.position.set(-1.2, 0, 0);
scene.add(cube);

// Torus knot
const knotGeometry = new THREE.TorusKnotGeometry(0.7, 0.2, 100, 16);
const knotMaterial = new THREE.MeshStandardMaterial({ color: 0xff8800 });
const knot = new THREE.Mesh(knotGeometry, knotMaterial);
knot.position.set(1.2, 0, 0);
scene.add(knot);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 10;
controls.target.set(0, 0, 0);
controls.update();

// UI
let autoRotate = true;
const resetCameraBtn = document.getElementById('resetCamera');
const toggleAutoRotateBtn = document.getElementById('toggleAutoRotate');

if (resetCameraBtn) {
  resetCameraBtn.addEventListener('click', () => {
    camera.position.set(3, 2, 4);
    controls.target.set(0, 0, 0);
    controls.update();
  });
}

if (toggleAutoRotateBtn) {
  toggleAutoRotateBtn.addEventListener('click', () => {
    autoRotate = !autoRotate;
  });
}

// Resize handling
window.addEventListener('resize', () => {
  const { innerWidth, innerHeight, devicePixelRatio } = window;
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
});

// Animation loop
function animate() {
  requestAnimationFrame(animate);

  if (autoRotate) {
    cube.rotation.x += 0.005;
    cube.rotation.y += 0.01;

    knot.rotation.x += 0.003;
    knot.rotation.y += 0.008;
  }

  controls.update();
  renderer.render(scene, camera);
}

animate();