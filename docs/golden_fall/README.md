# GOLDEN FALL — MICRO-MVP V0.9

**Status:** approved creative direction, proposed production plan; **not a playable game**. This package is a non-destructive handoff for an **existing Godot first-person prototype**, not a replacement Godot project.

**Player-facing language:** American English. **Working title:** *Golden Fall*. **Genre:** first-person Mystery Life Sim / psychological folk horror, NOT a dating sim. **Setting:** Morrow Creek, Oregon, October 2003; a golden-brown autumn whose continuity might be abnormal. **Art:** aggressively low-poly, Puppet Combo-like roughness with carefully directed light. **Audio:** *no spoken performances, no TTS*. On-screen text types in with restrained synthetic text blips specific to a character.

## What we are building *now*

A compact **three-day micro-vertical slice**, ~25–45 minutes as a hypothesis to test, ending after the playable horror event **THE REHEARSAL**. Playable spaces: the **existing bedroom**, **one short street**, the **diner + short service alley**. The PC (browser, journal, calendar, saves, messages) and bed/sleep already exist and MUST be preserved when functional. NO forest map, photograph-of-Evan twist, cloning reveal, monster, dating meters, full demo, forced cutscenes, voice acting or permanent HUD in this stage.

## Where to begin

1. Read `AGENTS.md` and `CODEX_START_PROMPT.md`.
2. Review `docs/00_CANON.md` and `docs/01_MICRO_MVP_GAMEPLAY.md` before writing a single new scene.
3. Read the event breakdown (`docs/02_THREE_DAYS.md`) and horror blocking (`docs/03_THE_REHEARSAL.md`) in full.
4. Inspect the existing repository first, mapping its scenes and scripts. Preserve and extend; never overwrite the repository with this reference pack.
5. Implement in small batches with playable review checkpoints, specified in `docs/09_PRODUCTION_AND_TESTS.md`.

## Active files (in priority order)

- `AGENTS.md` — must-follow technical and content rules for Codex
- `CODEX_START_PROMPT.md` — ready-to-paste handoff
- `docs/00_CANON.md` — creative vision and non-negotiables
- `docs/01_MICRO_MVP_GAMEPLAY.md` — actual loop, economy of attention/time and branching
- `docs/02_THREE_DAYS.md` — day-by-day beat sheet and player possibilities
- `docs/03_THE_REHEARSAL.md` — spatial staging, no-voice text horror and failure/exit paths
- `docs/04_CHARACTERS_AND_SCRIPT.md` — characterization and playable English dialogue examples
- `docs/05_DIALOGUE_UI_AND_BLIPS.md` — no portraits, no voice, text UX and procedural sound
- `docs/06_SPACES_ART_SOUND.md` — room, street, diner, service alley, asset constraints and mood
- `docs/07_COMPUTER_AND_WEB.md` — period PC as diegetic tool
- `docs/08_STATE_DATA_CONTRACT.md` — persistent data, sample JSON and adaptation guidance
- `docs/09_PRODUCTION_AND_TESTS.md` — phases, requirements, review and playtest criteria
- `docs/10_FUTURE_NOT_NOW.md` — deferred story/forest/romance ideas, no spoilers in MVP
- `docs/11_V08_MIGRATION.md` — differences from previous pack and dangerous obsolete instructions
- `data/` — sample authored English event/dialogue data, text-blip profiles, in-game messages, and state/test fixtures; **contracts/examples**, migrate to existing project's schema
- `tests/validate_pack.py` — static verification of package data, no Godot runtime required
- `reference/current_FPS_room.webp` — current early prototype screenshot; maintain its actual state
- `reference/Tokimeki_1994_historical_reference.md` — research for future life-sim structure, **NOT current scope**

## Important distinction

This zip includes **no repository code**, no executable demo, no generated 3D assets or audio. The Godot scene paths/structure remain unknown until Codex inspects *your actual code*. Never report source integrations, scene tests or playtests as completed before executing them.
