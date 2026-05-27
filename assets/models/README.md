# Fund Pilot — 3D models (GLB)

Curated **glTF/GLB** assets (Khronos Sample Assets, CC0-style reference models). Loaded via Three.js `GLTFLoader` with Fund Pilot gold/sage material grading and HDR-style lighting.

| File | Section | Model |
|------|---------|-------|
| `hero.glb` | Hero | Transmission glass spheres |
| `analyze.glb` | Analyze | Chronograph watch (precision) |
| `crm.glb` | CRM | Sheen chair (workspace) |
| `pilot.glb` | Pilot | Damaged helmet (metallic) |
| `dialer.glb` | Dialer | Boom box (audio/outbound) |
| `leads.glb` | Leads | Transmission plant (growth) |

## Upgrading to custom models (recommended long-term)

For **on-brand** Fund Pilot assets (logo-mark orb, laptop with your UI, Pilot avatar):

1. **[Spline](https://spline.design)** — design in browser, export **GLB**, drop into this folder.
2. **[Blender](https://blender.org)** — free, full control; export glTF 2.0 binary (.glb).
3. **[Sketchfab](https://sketchfab.com)** — filter CC0 / commercial-use; download GLB.
4. **[Poly Pizza](https://poly.pizza)** — CC0 low-poly props (laptop, phone, documents).

After adding a file, update paths in `js/fp-gltf-core.js` → `MODELS` map.
