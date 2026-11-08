# Ghost Hospital V1 — asset credits + verification notes (2026-11-07)

## Ghosts (Sketchfab, all CC-BY)
- Samara (The Ring) — CoryRichards — https://sketchfab.com/3d-models/samara-the-ring-57ab1a21d63744dfab12c54c7d139ddb — 4.4MB, 40k tris, 7.1m tall in file -> scaled to 1.7m at runtime
- Bubble Head Nurse — deankagura — https://sketchfab.com/3d-models/bubble-head-nurse-e11a8890356f48829b8114acf086214c — 2.0MB, 10k tris, 1.8m
- scary doll — vicente betoret ferrero (@deathcow) — https://sketchfab.com/3d-models/scary-doll-a4f41c0b7c8c4dd2be593b4b8ca8d075 — 2.3MB, 50k tris, 1.8m
- GBVGR Spider Witch (Ghost Form) — Zorg_Sinister — https://sketchfab.com/3d-models/gbvgr-spider-witch-ghost-form-904c894044f14334bd91e1264eeef0ce — 2.0MB, 7.8k tris

## Hospital (Sketchfab, all CC-BY)
- Low-poly Abandoned hospital — Alexandrovich — https://sketchfab.com/3d-models/low-poly-abandoned-hospital-21f2717e0f824b1fbc79205e549b1abb — 6.6MB, 99k tris, 14x33m, 2 storeys. Placed as the ruined building EAST of the playable wing (offset +14m X) so its interior never blocks gameplay; the playable floor is built from the modular kit.
- Abandoned Building Modular Environment Kit — olegolegperepelica — https://sketchfab.com/3d-models/abandoned-building-modular-environment-kit-376aead6cd3d41bda715cbab99c440fa — 2.3MB, 1.9k tris. 2m-grid pieces (walls 2m long x 3m tall, floor/ceiling 2x2). Baked + recentered at load (FBX cm + Z-up node transforms); merged into ~3 draw calls.

## Hand + sounds
- hand-real.glb (0.5MB) reused from the old hospital backup (small, not the 13MB hand-woman).
- 8 Freesound CC0 sounds, MP3 668KB total — see SOUNDS.md.

## Total load: ~21MB (ghosts 10.7 + hospital 6.6 + kit 2.3 + sounds 0.67 + hand 0.5 + index.html ~0.06)

## Verification done (Node, no GPU)
- Layout BFS (verify_v1.mjs): spawn->stair reachable on floors 15/1/8; every OPEN room reachable; closed rooms correctly unreachable.
- Ghost normalization (ghost_norm.mjs): Samara 7.1->1.7m, Doll 1.79->1.8m, Nurse 1.83->1.8m.
- WITCH LESSON (important): the spider-witch's SKELETON stands upright (pelvis y=3.4, head y=5.2) but its MESH renders lying flat (bind pose == rest pose, proven via inverseBindMatrices) — a long low spider creature, 5.3m long x 1.6m tall. Do NOT rotate it upright. It is a CRAWLER: scaled by length to 2.0m long, 0.6m tall, faceBack=true (head at -Z end, best guess). If it looks wrong on Zaw's phone, swap it.
- Kit wall truth: walls are 3m tall x 2m long (not 2x3) — the raw accessor bbox (0.09x2.00x3.00) is pre-transform; after the FBX node chain they are Y-up 3m tall. extractKitParts bakes matrixWorld + recenters.

## Props (Sketchfab, all CC-BY) — added V13
- Corpse — tamaldequezo — https://sketchfab.com/3d-models/corpse-be9b034525c246cebab3620acb5a8027 — 3.1MB, 624 tris, lying flat 2.1m -> scaled to 1.75m at runtime
- Old hospital bed (PBR|GR) — tris09 — https://sketchfab.com/3d-models/old-hospital-bed-pbrgr-3b2ccb0cc5fc4dda8c929300ccd3d49c — 15,922 tris, file in cm (180x130x234) -> scaled to 2.0m long; textures downscaled to 1024px + MR/normal maps stripped (37.8MB -> 1.9MB) for phone load
- Antique Wall Clock — 3DGunsmith — https://sketchfab.com/3d-models/antique-wall-clock-174a3fc826414bfc9693d9b00f43fe57 — 2.3MB, 1,970 tris, 0.4m round, wall-mounted in corridor
- Calendar Wall - 3MB — ahmagh2e — https://sketchfab.com/3d-models/calendar-wall-3mb-03df12d6917a406da7a2b3ee333faba6 — 4.2MB, 1,004 tris, 2.8m tall in file -> scaled to 0.45m, wall-mounted in rooms
