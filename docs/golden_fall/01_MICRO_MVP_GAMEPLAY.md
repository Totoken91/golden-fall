# 01 — MICRO-MVP GAMEPLAY: WHAT THE PLAYER ACTUALLY DOES

## The vertical-slice question

Can three small spaces and two low-poly people create an appealing daily-life loop so that a *single* incomprehensible event genuinely frightens the player? If not, scale DOWN, rewrite, and replay. Do not build more scenery as a substitute for finding the loop.

**Target** (not a validated runtime): three in-game days, 25–45 real minutes; room, main street, diner, diner service alley; June and Hannah; one major horror scene. No repetitive morning/school simulations. Date advances only on using the real bed, with player confirmation; the actual clock advances discreetly after substantive commitments. Idle walking, web reading and inspecting do NOT burn time. Do not punish slow readers.

## One coherent loop, not three genres

1. **Be there:** move in a real space, notice person/objects/habits, enjoy rain and music.
2. **Talk or interact:** optional believable small talk, small decisions with remembered consequences; no romantic point grind.
3. **Check something:** optionally use desktop Web/messages/journal; the PC is a tool, not a daily activity selector.
4. **Choose to return or leave:** people and available conversation change by date/choice.
5. **Sleep:** tomorrow's state changes; use the next day to revisit a familiar place with a new context.
6. **The intrusion:** an event is frightening precisely because the ordinary loop became recognizable.

## Actual decisions in this MVP

- Day 1: pick an answer to June; optionally get acquainted with Hannah and discuss her imperfect roll of film. Both return with callbacks if encountered again.
- Day 2: choose to visit diner again and ask Hannah about her camera, or browse local Web first; one topic becomes available when remembering an ordinary detail. The player can refuse and sleep instead; no mandatory lore gates.
- Day 3: Hannah's important two-beat conversation provides two player-selected response strings, each recorded exactly; one response affects her casual goodbye. Later (if the player walks around the back) those **chosen words** appear again as `???`. The player may approach, listen, retreat, fetch June or depart; the event is not a button labeled "Investigate anomaly".
- Return home: journal distinguishes personally witnessed facts from rumors, offers no author explanation; the player can close the PC and sleep. End-of-micro-MVP screen occurs after quiet return, *not* at a monster face or plot twist.

## Time model

Three persistent day indices (0, 1, 2): Wednesday/Thursday/Friday Oct 15–17, 2003. A day begins late afternoon (`16:10`) when leaving school is implicit (no school interior in MVP). Friday diner event can be offered near evening after conversation; game-clock time may advance during committed social interaction. Bedroom always accessible. A reasonable fictional time string on wristwatch or PC is enough; do not flood the screen with timers. No real-time expiration while reading dialogues or searching websites.

**Day progression:** A sleep confirmation advances exactly one day; on the final day it can end the micro-MVP with a simple neutral end screen after returning home. Never force the final sleep if the player wants to linger. If the player has skipped horror entirely, mark this branch as `rehearsal_unseen` and allow a short neutral end rather than fabricating knowledge.

## The accessible player state

No permanent checklist/HUD. Computer journal can reflect what happened using first-person observational language; never provide omniscient diagnosis. Gameplay choices must have at least TWO visible callbacks: e.g., Hannah's response on day 2 to an earlier photo question; June's greeting on day 3 if the player was curt vs friendly. These are small but real: the town has a memory.

## How to avoid walking-simulator boredom

- Design under 2 minutes traversing room→diner at ordinary walking speed; allow direct street transitions without fade labyrinths.
- Make diner props inspectable only where they have a purpose (photographs, noticeboard, radio/record, closing note) or personality. Avoid hundreds of empty interaction prompts.
- At least one free observation unrelated to horror rewards attention: the rain on the window, record request board, a personal sketch, silly customer note.
- No spoon-moving compulsory puzzle and no mandatory fetch quests.
- First return visit yields altered dialogue/environment. Second visit must not be identical; otherwise three days are filler.
- Optional internet research contextualizes the town but should not spoil disappearance plot in this slice.

## Failure/skip states

Player who misses Hannah on day 1 can still meet her on day 2/3. Day 3's pivotal conversation must be readily available via natural staging, but NOT automatically start upon entering diner. The Rehearsal only has **personal choice replay** if the pivotal dialogue is completed; never fabricate the player's words from another route. If player skips, provide a shorter ambient version using an already overheard exchange (not falsely personal), or let them miss the event; test discovery rate. No permanent lockouts, collision traps or unfinishable days.
