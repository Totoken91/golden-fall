# CODEX START — GOLDEN FALL V0.9 MICRO-MVP

You are continuing my existing Godot **first-person** project, now working-titled **Golden Fall**. The current repository already contains a bedroom, a simulated 2003 computer (browser/research, journal, agenda, save), and a bed/sleep-to-next-day interaction. I may also have work in progress on a street and diner.

This package is the NEW authoritative creative specification, superseding V0.4–V0.8. First read `AGENTS.md`, `README.md`, `docs/00_CANON.md` through `docs/11_V08_MIGRATION.md`, and review `data/*.json`. The Tokimeki analysis in `reference/` is historical inspiration, not the current build request.

**FIRST, audit my actual repository without modifying it**: list the existing paths/scenes/systems and their state, show what can be reused and exactly how you will integrate this micro-MVP, and checkpoint the current build. Do not assume the reference ZIP itself is a complete game. Keep all existing functional computer, save, bed and movement code.

**THEN implement ONLY the three-day micro-MVP** described in the docs: a 2003 Oregon golden-autumn street, a compact diner, the existing bedroom, two extremely low-poly NPCs (June and Hannah), natural English dialogue with NO 2D portrait panels, NO voice recordings or TTS, subtle per-character text blips, meaningful remembered dialogue choices, and finally the deeply unsettling diegetic text-only horror set-piece **The Rehearsal** in the service alley. Selected protagonist lines reappear under **`???`**, NEVER `YOU`. Do not explain what the voices/text mean. The player must be able to observe, approach, withdraw or leave. No jumpscare, visible entity or "practicing" exposition.

Use the sample data as contracts/examples and translate to the repository's architecture rather than forcing a rewrite. Develop in phases: (1) room↔street↔diner traversal and lighting; (2) two believable conversations with persistent choices; (3) ambient offscreen text/sound grammar; (4) The Rehearsal; (5) save/reload/skip/accessibility/playtests. Each phase must be playable and produce a clear DEVLOG entry.

Before starting phase 4, show me an in-engine capture of the alley layout and a sample of real dialogue UI and blip behavior for approval. Report only things you actually tested. Stop after the micro-MVP; do NOT build the full demo or the photographic reveal.
