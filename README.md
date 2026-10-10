# Golden Fall

First-person mystery life sim with quiet folk horror. Morrow Creek, Oregon, October 2003.
Godot 4.6 (GL Compatibility), low-poly PSX look, no voice acting.

**Status:** early prototype (V0.22). The bedroom, the period computer (calendar, journal, messages,
saves, an offline 2003 web) and the three-day sleep loop (Wed Oct 15 – Fri Oct 17) are playable.
The street, the diner, June, Hannah and the Friday event come next
(see `docs/golden_fall/09_PRODUCTION_AND_TESTS.md`).

## Play

- **In a browser:** the `web/` folder is a static export (no threads, no special headers), deployed on Vercel.
  Click the game once to capture the mouse and enable sound.
- **On Windows:** open `game/` in Godot 4.6 and run, or export with the "Windows Desktop" preset.

Controls: WASD / ZQSD to move, mouse to look, E to interact, Esc to pause.

## Layout

| Path | Contents |
|---|---|
| `game/` | Godot project: scenes, scripts, shaders, data (`game/data/*_en.json`), imported assets |
| `web/` | Web export served by Vercel (`vercel.json`) |
| `docs/golden_fall/` | Authoritative creative and production spec (V0.9 micro-MVP) |
| `docs/legacy_heures_creuses/` | History of the earlier French prototype, incl. the zone-building guide (doc 22) |
| `assets/blender/`, `scripts/assets/` | Blender sources and the bpy scripts that build the models |
| `scripts/textures/` | Texture pipeline (Poly Haven / ambientCG official APIs) |
| `scripts/qa/golden_check.gd` | Engine QA for the home loop |
| `tests/` | Python checks (data contracts, encoding, assets, texture pipeline) |

## Checks

```
godot --headless --path game --export-pack "Windows Desktop" <abs>/play/GoldenFall.pck
LHC_QA_DIR=<dir> LHC_CAMPAIGN_SAVE=<dir>/save.json LHC_CAMPAIGN_STAGE=day1 \
  godot --main-pack <abs>/play/GoldenFall.pck --script scripts/qa/golden_check.gd -- --campaign-check
```

Run stages `day1`, `day2`, `day3` in order. The bedroom regression suite:
`godot --main-pack GoldenFall.pck res://scenes/room_review.tscn -- --room-check`.
Python: `python -m unittest discover tests`.
