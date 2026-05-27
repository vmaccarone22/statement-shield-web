import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

export var MODELS = {
  hero: "assets/models/hero.glb",
  analyze: "assets/models/analyze.glb",
  crm: "assets/models/crm.glb",
  pilot: "assets/models/pilot.glb",
  dialer: "assets/models/dialer.glb",
  leads: "assets/models/leads.glb",
};

var loader = new GLTFLoader();
var cache = new Map();

export function createRenderer(canvas) {
  var renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  return renderer;
}

export function createCamera(fov) {
  var camera = new THREE.PerspectiveCamera(fov || 38, 1, 0.1, 100);
  camera.position.set(0, 0.15, 5.2);
  return camera;
}

export function addBrandLights(scene) {
  scene.add(new THREE.AmbientLight(0xfff5e8, 0.35));
  var key = new THREE.DirectionalLight(0xffe4b5, 1.35);
  key.position.set(4, 7, 6);
  scene.add(key);
  var fill = new THREE.DirectionalLight(0x8eb69b, 0.45);
  fill.position.set(-5, 2, 4);
  scene.add(fill);
  var rim = new THREE.PointLight(0xd4af73, 0.85, 28);
  rim.position.set(0, -2, -3);
  scene.add(rim);
}

export function applyStudioEnvironment(renderer, scene) {
  if (scene.userData.envApplied) return;
  var pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();
  var env = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environment = env;
  scene.userData.envApplied = true;
  scene.userData.pmrem = pmrem;
}

export function loadModel(url) {
  if (cache.has(url)) return cache.get(url);
  var promise = new Promise(function (resolve, reject) {
    loader.load(
      url,
      function (gltf) {
        var root = gltf.scene;
        normalizeRoot(root, 2.4);
        applyBrandGrade(root);
        resolve({ root: root, animations: gltf.animations || [] });
      },
      undefined,
      reject
    );
  });
  cache.set(url, promise);
  return promise;
}

export function normalizeRoot(root, targetSize) {
  var box = new THREE.Box3().setFromObject(root);
  var size = box.getSize(new THREE.Vector3());
  var maxDim = Math.max(size.x, size.y, size.z) || 1;
  var scale = targetSize / maxDim;
  root.scale.setScalar(scale);
  box.setFromObject(root);
  var center = box.getCenter(new THREE.Vector3());
  root.position.sub(center);
}

export function applyBrandGrade(root) {
  root.traverse(function (child) {
    if (!child.isMesh) return;
    child.castShadow = false;
    child.receiveShadow = false;
    var mats = Array.isArray(child.material) ? child.material : [child.material];
    mats.forEach(function (mat) {
      if (!mat) return;
      if (mat.isMeshStandardMaterial || mat.isMeshPhysicalMaterial) {
        mat.metalness = Math.min(1, (mat.metalness || 0) + 0.15);
        mat.roughness = Math.max(0.12, (mat.roughness || 0.5) * 0.82);
        if (mat.isMeshPhysicalMaterial) {
          mat.clearcoat = Math.max(mat.clearcoat || 0, 0.35);
          mat.clearcoatRoughness = 0.18;
        }
        if (mat.color) {
          var hsl = { h: 0, s: 0, l: 0 };
          mat.color.getHSL(hsl);
          if (hsl.s < 0.08) {
            mat.color.setHex(0xd4af73);
            mat.metalness = Math.max(mat.metalness, 0.55);
          } else if (hsl.h > 0.08 && hsl.h < 0.55) {
            mat.color.lerp(new THREE.Color(0xd4af73), 0.22);
          }
        }
      }
      if (mat.isMeshPhysicalMaterial && mat.transmission > 0) {
        mat.thickness = Math.max(mat.thickness || 0, 0.5);
        mat.ior = 1.45;
        mat.attenuationColor = new THREE.Color(0xd4af73);
        mat.attenuationDistance = 2.5;
      }
    });
  });
}

export function addGoldParticles(scene, count) {
  count = count || 280;
  var positions = new Float32Array(count * 3);
  for (var i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 14;
  var geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  var pts = new THREE.Points(
    geo,
    new THREE.PointsMaterial({
      color: 0xd4af73,
      size: 0.028,
      transparent: true,
      opacity: 0.42,
      depthWrite: false,
    })
  );
  scene.add(pts);
  return pts;
}

export function resizeRenderer(renderer, camera, canvas) {
  var w = canvas.clientWidth;
  var h = canvas.clientHeight;
  if (!w || !h) return false;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  return true;
}
