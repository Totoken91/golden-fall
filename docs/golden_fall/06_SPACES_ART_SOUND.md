# 06 — ENVIRONMENTS AND GOLDEN AUTUMN GOTHIC ART

## Scope: small but intentional

**R0 — Existing bedroom**: protect its geometry, existing CRT computer interaction, journal/save/calendar, bed sleep, camera. The creator's screenshot is included in `reference/`. Improve only after audit; fix actual blockers before embellishing. Window rain, amber lamp glow, wall and desk clutter with a personal history, but avoid transforming the room into a haunted exhibit. Make sure PC remains readable and interaction/cursor return works.

**R1 — Main street**: one short walkable 60–100m segment, no fake infinite city or four season asset variants. A coherent pedestrian route room→diner and back. Two or three building facades, parked 1990–2003 cars, wet golden-brown leaf material, wires/telegraph poles, dark spruce wall behind warm deciduous leaves, late-afternoon shafts and orange streetlamps. Diner must visibly invite player in. Don't block paths with invisible collision. Distant backgrounds can be simple painted planes/skybox; no full simulated traffic necessary.

**R2 — Morrow Diner**: 6–8m width and 10–14m length as **placeholder guidance**, adapt to actual assets. Counter, coffee machine, 3–4 booths, one window seat for Hannah, June at counter, rear kitchen implied behind swing door, main entrance and visual access to its exterior. Ordinary lived-in detail: coffee rings, slightly dirty windows, mismatched mugs, handwritten specials board, 2003 notices, thrifted amber light. Don't create suspicious ghost props that foreshadow the setpiece. Layout must permit line of sight when approaching both characters and easy navigation with FPS capsule.

**R3 — Service alley**: 10–18m short external corridor/turn around diner, accessible from street without loading a new level, set dressing from a few re-usable meshes; compressor hum, wet brick, service lamp, vent, closed service door. The source of strange text is **offscreen and never visible**. Players can inspect door but never see a hidden actor/copycat. Retain escape route at all times.

## Rendering rules

- Extremely low-poly proportions and deliberately low-resolution textures. Puppet Combo-like **roughness**, not hyperreal PS2 character faces. More detailed concept images from old versions are COLOR/CAMERA refs only; NOT target poly counts or direct render matches.
- Aim for readable silhouettes, restrained vertex counts, rough PS1/PS2 material language, 64–256px atlased textures where suitable (guidance, not universal cap). Avoid excessive photoreal normal maps, plastic materials, over-polished PBR reflections.
- Do not confuse atmospheric darkness with unplayable black walls. Keep silhouettes, door frames, route boundaries and interactables distinguishable; no overpowered CRT-style grain preventing text reading.
- Preserve amber/brown palette in **all** places; outdoor fog may be gray and trees dark green, not blanket blue filter. Lighting and color-temperature shifts separate late afternoon, diner warmth, damp alley darkness. One autumn asset set with weather/time variations; no snow, summer, spring versions.
- No need to solve intricate animation; two figures with minimal idle/head turns and simple walking/exit path. A single re-usable rig is fine if mesh proportions differ enough to recognize people.

## Blender/Codex workflow, only if needed

Generate simple props and modular buildings via Blender Python in background, keep `.blend` editable source and export GLB to Godot. Blender MCP is optional; Codex should prefer tools actually available and not block on a cloud service, auto-rig API or Mixamo dependency. Existing models/asset licenses must be checked. Build prop families (tables, poles, fallen leaves, streetlamp) with shared materials. Verify GLB scale/orientation, UVs, bounds, collision and renders from gameplay camera. No requirement to generate unique high-resolution organic models.

## Ambient sound as story, NOT recorded voices

- Music: original or properly licensed restrained lo-fi folk guitar/slowcore fragments, sparse/quiet inside. Silence and low ambient layers count as composition. No copying commercial songs.
- R1: distant occasional vehicles, wind moving autumn leaves, light rain, intermittent crow perhaps, no constant dramatic drone.
- R2: refrigerator, espresso/coffee apparatus, dishes ceramic ticks, faint radio/music, ambience through rain on window, exterior traffic reduced.
- R3: exhaust/fan, drain dripping, distant traffic; sound need not move as the text source does. No diegetic spoken lines.
- Typewriter bleeps: nonverbal 2D UI tones, per speaker, rate-limited. No TTS/VO/language mimic.

## Level review captures Codex must provide

For each milestone, capture at least: daylight street from room direction, diner storefront at dusk, seated Hannah viewpoint, June counter viewpoint, alley approached at night, the bedroom at night/PC open, typography/blip demo screenshot. Gameplay capture and real performance matter more than still concept art.
