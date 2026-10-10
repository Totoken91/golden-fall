# 09 — CODEX PLAN, MILESTONES, TESTS, REVIEW GATES

## Step 0: non-destructive repo audit (STOP before implementation)

List all scene/script/resource paths of current project. Identify what works in current room, PC and sleep. Verify engine and renderer version, FPS controls, resolution, input mode, current file data contracts, save file location. Check if Codex already added street/diner assets. Present a small migration map with impact and risks. Commit/back up working state. **No blind project replacement.**

## Stage 1: golden-town traversal, actually playable

Room door -> 60–100m street -> diner entrance -> return. Make autumn lighting, collisions, camera scale, seamless door/scene transitions and sound transitions credible; no voids/z-fighting, camera clipping or 5-minute walk. Verify return to room, PC and sleep unchanged. Creator approval checkpoint: street and diner entrance screenshot + 30s capture.

## Stage 2: believable humans & continuity

Add June/Hannah low-poly meshes (temporary strongly-stylized blockout allowed but label as such), idle and 1–2 gestures. Implement player-triggered conversation UI, TypeBleepPlayer, two-day callbacks, ambient subtitling without portraits and without voices. Two real choices influence next day response. Test both normal and offscreen channel. Creator approval checkpoint: in-game conversation and blip audio capture (video); no need to judge horror yet.

## Stage 3: real Friday route

Two-choice pivotal conversation, store selections, Hannah physical departure and availability state; make service alley accessible and visually readable. Write a test harness that asserts correct selected strings are in saved state. Do NOT implement supernatural behavior until stage 2 demonstrates the ordinary dialogue format credibly.

## Stage 4: The Rehearsal (one short setpiece)

Single offscreen subtitle system stages familiar Hannah line → exact selected player line under `???` → exact Hannah reply → *very spare* authored fragments/pauses → silence. Player freely explores, exits, returns. No VO/TTS, horror stinger, animation reset, door jump, jumpscare, revealed threat or explicit practice language. Stage cues from a durable state machine. Creator tests fear/awkwardness before further polish.

## Stage 5: completion + technical/human playtests

Bedroom return, factual optional journal note, bed finish, save/load/sleep, reload with partial Rehearsal, accessibility settings, no missing subtitles at rapid movement, no infinite trigger repetition. Tune blip frequency and pace. Have at least **3 cold testers** (recommendation) describe scene without being told its meaning; ask whether they recognized their choice and whether the dialogue felt like a bug. If it feels like a bug, fix presentation/foreshadowing/pacing before adding more horror.

## Mandatory tests

| ID | Check | Pass criterion |
|---|---|---|
| P01 | Existing home retained | Bedroom, CRT PC, browser, journal, save, sleep still functional |
| P02 | FPS travel | Room→street→diner→alley→room, no missing collisions/z-fighting |
| P03 | English-only | All visible UI, messages, dialogue in US English |
| P04 | No portraits/voice | No 2D dialogue portraits, no spoken audio or TTS anywhere |
| P05 | Text bleep settings | Sound distinct by speaker, unobtrusive, disabled cleanly; readability unchanged |
| P06 | Day progression | Sleep moves exactly 1 day, no day skip after reloading |
| P07 | Remembered social choice | At least 2 non-cosmetic later response variations |
| P08 | Ambient subtitle grammar | Ordinary offscreen speech is displayed before Friday scene |
| P09 | Exact chosen text | Friday replay uses selected choice text verbatim under `???` |
| P10 | Branch coverage | All 3 first answers & all 3 second answers work, no wrong replay |
| P11 | No spoiler labels | `REHEARSAL`, `COPY`, `ENTITY`, `YOU` not visible in horror scene |
| P12 | Leave and return | No forced camera, repeat spamming, or player softlock |
| P13 | Save mid-event | Resume stage; no restart of already-read first beat |
| P14 | No premature content | No photo-of-Evan reveal, no giant forest level or monster |
| P15 | Calm after horror | Can return bedroom, voluntarily end and use PC as normal |
| P16 | Readability | Dialogue legible at target resolution while in motion / with bleep off |
| P17 | Ordinary loop | No 'press Study, then sleep' button workflow |
| P18 | Subjective efficacy | Blind players understand that exact response returns; can't easily reduce scene to bad AI/bug |

## Kill switches and rollback

Feature flags: `ENABLE_REHEARSAL`, `ENABLE_TYPE_BLEEPS`, `ENABLE_FRIDAY_SCENE`, and `DEBUG_EVENTS` can isolate systems during tests. If asset pipeline or animation blocks core loop, use simple placeholders with stable layout. If stage 4 is not scary, prototype 2–3 timing/line variants locally but do not automatically expand scope or add jump scares.
