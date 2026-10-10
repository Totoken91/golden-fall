# 11 — MIGRATION FROM PREVIOUS PACKS

This is a **clean new direction**. Previous versions do not contain the authoritative build spec. Do not copy their old instructions into current `AGENTS.md` or execute them. The older files may still be useful as historical research if an explicit question arises.

| Previous concept | Current V0.9 status |
|---|---|
| *Les Heures Creuses* name | **Golden Fall** working title, US-English game |
| Old Tokimeki stat/calendar dating loop | Historic research only; no seduction grind or PC-study button |
| 3rd-person exploration | Superseded: FIRST PERSON as current prototype |
| 2D illustrated VN portraits | Superseded: no dialogue portraits; in-world retro paper/screens fine |
| Detailed PS2 facial/body animation | Superseded: deliberately extreme low-poly, minimal poses |
| Sound-recorded Hannah/player voices | Superseded: **NO voice acting, NO TTS**; typewriter text bleeps only |
| `YOU` subtitle in back-alley horror | Superseded: always `???` for unknown repeating selected words |
| Entity "practicing" revealed as premise | Superseded: incomprehensible, never identified or explained |
| V0.8 `Second Closing` cup/June loop | REJECTED: too much like NPC script bug |
| V0.8 4-day photo cliffhanger | DEFERRED: future larger demo, no final photo in micro-MVP |
| `Someone Came Home` doppelganger | REJECTED: gives away mechanism too early |
| `The Conversation We Never Had` | REJECTED: a weaker echo of The Rehearsal |
| V0.8 room/street/diner continuity | KEEP, adapt to 3-day micro-MVP |
| 2003 Web, notebook, saves, bed | KEEP existing implemented systems |
| Blender procedural asset pipeline | Optional support; low-poly constraints take priority |

Suggested migration procedure:

1. Existing Godot project remains the source of executable truth. Inspect repo for `AGENTS.md`/pack docs: merge current guidance while preserving useful local build commands and code ownership conventions.
2. Make a Git checkpoint. Keep old data files under `legacy/` only if code references them; do not leave obsolete `Second Closing` active event data enabled.
3. Add/migrate new data behind versioned schemas or adapters rather than breaking currently working saved games.
4. Implement one phase at a time; do not import nested older ZIP archives or overwrite the existing game root with this package.
5. Confirm that no player-facing plot twist from old version leaks into new NPC dialogue, PC pages, posters, or debug UI.
