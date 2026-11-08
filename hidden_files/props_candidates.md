# Props for Ghost Hospital V12 — Sketchfab candidates (2026-11-08)

Zaw asked for REAL models (not code-drawn): corpse, hospital bed, wall clock, wall calendar.
All 4 primaries were picked from thumbnails (viewed) + Sketchfab API (licence/tris verified).
All are CC-BY (attribution required — add to ASSETS.md / footer credits on wiring).

## DOWNLOAD BLOCKER — read first
Sketchfab's download API (`GET /v3/models/{uid}/download`) returns **401 without a
logged-in token** (tested GET + POST, browser UA + Referer, CC-BY and CC0 — all 401).
The viewer/embed route only exposes proprietary OSGJS binary (`file.binz` + an opaque
blob) — NOT convertible to GLB. There is NO no-login download route.
**So: download these 4 in the VM browser (logged in as 'Cjkgdfjjhh'):**
for each URL below → "Download 3D Model" → choose **glTF** format → save the ZIP.
Then convert each ZIP to GLB with the packer (tested, stdlib-only):
  python3 hidden_files/gltf_to_glb.py /path/to/unzipped-model-dir props/corpse.glb
  (repeat for bed / clock / calendar)
Then verify each with: node hidden_files/glb_info.mjs props/<name>.glb
and record the bbox dims here before wiring into index.html.

## PRIMARY PICKS (download these)
### 1. corpse.glb — "Corpse" by tamaldequezo (CC-BY)
- URL: https://sketchfab.com/3d-models/corpse-be9b034525c246cebab3620acb5a8027
- 624 tris, 339 verts, 0 anims, viewer modelSize ~5.6 KB (tiny — expect glTF ZIP < 1 MB)
- Thumbnail verdict: a bloody shrouded body LYING DOWN (long blood-stained cloth, lumpy
  body shape underneath). Realistic, creepy, clearly a corpse. Pure corpse (no gurney),
  so it can lie on the floor or on a bed. Expected bbox ~1.7 m long lying flat.
### 2. bed.glb — "Old hospital bed (PBR|GR)" by tris09 (CC-BY)
- URL: https://sketchfab.com/3d-models/old-hospital-bed-pbrgr-3b2ccb0cc5fc4dda8c929300ccd3d49c
- 15,922 tris, 12,303 verts, 0 anims, viewer modelSize ~121 KB (expect glTF ZIP ~1–2 MB)
- Thumbnail verdict: rusty old metal-frame bed with a plaid blanket — genuinely
  abandoned-hospital look, PBR, game-ready. The best-looking old bed found.
  NOTE: heaviest of the four (15.9k tris); used 6x/floor = ~95k tris. Acceptable for
  the scene (~200k total) but if phone FPS dips, swap to the jarapozo backup (526 tris).
  Expected bbox ~2.0 m long x ~0.9 m wide x ~0.8 m tall.
### 3. clock.glb — "Antique Wall Clock" by 3DGunsmith (CC-BY)
- URL: https://sketchfab.com/3d-models/antique-wall-clock-174a3fc826414bfc9693d9b00f43fe57
- 1,970 tris, 1,121 verts, 0 anims, viewer modelSize ~10 KB (expect glTF ZIP < 0.5 MB)
- Thumbnail verdict: ROUND wall clock, wooden rim, Roman numerals, cream face —
  antique, fits an old hospital wall. Expected bbox ~0.35–0.45 m diameter, flat
  (mount on wall, face pointing into the room, +Z or -Z depending on wall).
### 4. calendar.glb — "Calendar Wall - 3MB" by ahmagh2e (CC-BY)
- URL: https://sketchfab.com/3d-models/calendar-wall-3mb-03df12d6917a406da7a2b3ee333faba6
- 1,004 tris, 525 verts, 0 anims, viewer modelSize ~7 KB (expect glTF ZIP < 0.5 MB)
- Thumbnail verdict: a proper HANGING wall calendar (floral design, "2024" header,
  full-year grid, hanging by a string). Reads instantly as a wall calendar.
  Expected bbox ~0.3–0.4 m wide, flat (mount on wall like the clock).
  NOTE: the year on it reads 2024 — fine for an abandoned hospital.

## BACKUPS (if a primary fails to download / looks wrong in-game)
- corpse: "Dead Body" by LukasBobor (CC-BY, 1,816 tris)
  https://sketchfab.com/3d-models/dead-body-fdfca2c19a784789804f39d24f25bd8c
  Corpse on a wheeled gurney under a white sheet, bare feet sticking out — very
  hospital, but includes the gurney (bigger prop, use as a standalone gurney-corpse).
- bed: "Old and worn out hospital bed" by jarapozo (CC-BY, 526 tris)
  https://sketchfab.com/3d-models/old-and-worn-out-hospital-bed-b30a6e69d5d849c78abb2f760791c0d1
  Rusty bed, blood-stained mattress, very light. Use if the tris09 bed hurts FPS.
- clock: "Wall clock" by maximmihajlovich (CC-BY, 7,244 tris, 1 anim)
  https://sketchfab.com/3d-models/wall-clock-416c39a6670c493990585b1e198e533b
  Clean round clock, black rim, white face. Modern look; the 1 anim is probably the
  hands (ignore it — the game uses the static pose).
- calendar: "Wall Calendar / Tear off, with wind blowing" by gokulsanjeevan (CC-BY, 988 tris)
  https://sketchfab.com/3d-models/wall-calendar-tear-off-with-wind-blowing-1cfb64b810d14c089e6a0480a8bbb58a
  Tear-off calendar with a flapping page (Malayalam text on the page). Weaker pick —
  the thumbnail angle is odd and the page text is Malayalam.

## REJECTED (checked, do not use)
- "Corpse dead body" by Tired Software — Free Standard licence (NOT CC-BY/CC0).
- "Classic Wall Clock" by lucss_3d — CC-BY-NC (non-commercial; game is public).
- "Horror Corpse" by NomedaRepsaite — a STANDING bloody figure (T-pose), not lying down.
- "Corpse" by AaronJC — two wrapped mummies standing upright.
- "Low Poly Dead Body Covered" / "Covered Dead Body" — sheet lumps, less convincing than
  the tamaldequezo bloody shroud (and "low-poly" is what Zaw rejects).
- "Hospital Bed" by loxfear / ThreeDeeCreation — clean/modern beds, wrong vibe for an
  abandoned hospital (tris09 / jarapozo are the old ones).
- "Wall clock" by itsbroccoletto (33.6k tris) / HQ3DMOD (36k) — too heavy for a wall prop.

## Wiring notes for the parent (when the GLBs land in props/)
- Run glb_info.mjs on each; record bbox + tris here. Scale by longest dimension:
  corpse ~1.7 m long (lying flat — check whether it lies on XZ or stands on Y; rotate
  x=-PI/2 if it comes in standing), bed ~2.0 m long, clock/calendar ~0.35–0.45 m.
- Clock + calendar: flat wall mounts — place on room walls (y ~1.6–1.8 m), face into the
  room. The kit walls are at x=±6 / z=±15 and room walls; reuse the room-wall placement.
- Corpse replaces makeCorpse's code-built body; bed replaces makeBed's code-built frame.
  Keep the existing colliders (bed collider, corpse interact radius) — only swap the mesh.
- Total new load estimate: bed ~1–2 MB + corpse/clock/calendar < 0.5 MB each → ~2–3 MB
  added to the ~20 MB game. Fine.
- Credits to add to ASSETS.md: tamaldequezo, tris09, 3DGunsmith, ahmagh2e (all CC-BY).
