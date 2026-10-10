# 03 — THE REHEARSAL — HORROR DIRECTOR'S SPECIFICATION

**Private production codename only; do not present it in game.** Core emotion: *cosmic incomprehension*, not "a monster practicing human conversation." No monster intent, no voice acting, no copies of the protagonist on screen, no mechanical glitch reveal. Player's mind should resist classifying the event.

## A. Rules of sensory perception in a NO-VO game

1. All game spoken exchanges are represented as typed **English subtitle/dialogue text**, accompanied by character-specific, very restrained text bleeps. There are **no human speech recordings**. This is an established game convention; not to be literally interpreted as reading a supernatural screen.
2. On Days 1 and 2, ordinary characters chatting offscreen use the same subtitling conventions; spatial eligibility based on distance and plausible occlusion.
3. During this scene, show no portrait/cutscene/cinematic blackout to introduce a new mode. Same textbox style, same sound rules, same FPS camera.
4. `HANNAH` means "sounds/reads like Hannah" from the protagonist's perspective, never objective proof of speaker identity. `???` is an **unknown source**. Every replay of a player-selected choice must use `???`, NEVER `YOU`, `PLAYER`, the player's name or a visible human duplicate.
5. The distinct little bleeps are **not** language or a synthesized recorded voice. No imitation of the user's voice. Preserve uncertainty by making `???` musically plain/ambiguous, never stereotypical demonic/gravelly/robotic.

## B. Geometry, not a cutscene

- Same diner scene and adjacent street; use a **10–18 m service alley** behind or alongside building, reachable from the main street with ordinary navigation. No teleports.
- A plausible service door, drain, duct/extractor, wet ground, service light, one rubbish bin. The voice/text originates ambiguously from beyond the door/wall area, never an enemy model position that can be raycast and exposed.
- Player can approach/withdraw or inspect door; no forced camera movement. The door is locked normally, with an understated non-horror feedback such as `It won't open.` Avoid "Someone is holding it from the other side" explanatory text.
- Fade text volume/readability with proximity, but never make core lines impossible to read at typical walking speed; hold the first two familiar lines until seen OR revisit within an eligibility window. No repeated full audio if the player moves across a threshold.
- Unrelated environmental bed: gutter drops, distant traffic, fryer extractor hum, rain, compressor. A moment of sound loss can occur naturally; **no loud stinger, no breathy monster track**.

## C. Emotional pacing / authored beats (not a rigid on-rails cinematic)

**Beat 0 — Normality:** player has finished a natural diner conversation and Hannah physically leaves by the front entrance. At least 25–40 seconds of ordinary freedom and ambient life. No scripted "go behind the diner" instruction. A mundane reason to walk around the back: a shortcut home or curiosity about street layout.

**Beat 1 — Recognition, very quiet:** `HANNAH` uses exactly one previously heard **Hannah line**, same punctuation and timing conventions; subtitle originates near rear wall. The player may believe she is still nearby.

**Beat 2 — Personal impossibility:** `???` uses the **verbatim choice text actually chosen by player** in that preceding conversation. It has to be verbatim, not generic fallback or paraphrase. Do not write `YOU`. A line back from `HANNAH` follows; now the match is unmistakable.

**Beat 3 — No understandable grammar:** With irregular pauses, Hannah's text resumes with strange truncation, re-opened syllables and intact natural phrases: e.g. `I almost...` / `I al— I almost didn't...` / `I almost didn't come tonight.` Repeated microfragments should be short and curated, not spammed. A split between `HANNAH` and `???` may cause a *single phrase* to be completed across the two source tags. Don't call attention to it with visual glitches.

**Beat 4 — Unanswered silence:** the text stops without a voice warning, movement toward the door or jump. A barely perceptible environmental detail can remain: exhaust fan continues or stops; water drips. Player can attempt to look around, wait, exit, re-enter. They are not informed of what they witnessed.

**Beat 5 — Consequence:** If player questions June, she replies like an actual person dealing with odd questions: `I haven't seen her since she left. Why?` / `I was in the kitchen. I didn't hear anything over the fan.` Her response may depend on whether she was nearby. She does NOT report "an entity", a double, ghosts, or a time loop. The journal may record the **firsthand** fact of matching lines, never a theory.

## D. Sample text grammar (layout reference; game dialogue is authored in `data/dialogues_en.json`)

Prior conversation in the diner:

`HANNAH` — `I almost didn't come tonight.`
Player chooses: `Bad day?`
`HANNAH` — `Nothing dramatic. I just kept putting my shoes on and taking them off.`

Alley, same text style:

`HANNAH` — `I almost didn't come tonight.`
`???` — `Bad day?`
`HANNAH` — `Nothing dramatic. I just kept putting my shoes on and taking them off.`

Then a short silence and a deliberately **non-explanatory** fragment:

`HANNAH` — `I almost... I al—`
`???` — `...most didn't come tonight.`

Do NOT print “The voice is practicing”, “Something is copying us”, “The same conversation plays again”, “She isn't really Hannah”, “Why is it saying my lines?” or a detective-style UI clue. Player is trusted to notice.

## E. Finite event state machine

`DORMANT` -> `ELIGIBLE` (Hannah conversation completed; she exited; evening)
-> `SEEN_FIRST` (initial recognized line exposed)
-> `SEEN_REPLY` (actual choice played as `???`)
-> `DISTORTED` (strange fragments)
-> `SILENCE` -> `AFTERMATH`.

Walking away does not restart. On returning, show remaining fragments or ambient silence as appropriate. If player leaves during first line, optionally preserve first line as not yet "understood" and play from next legible beat; no 20-second audio loop or teleported phrase. All transitions must survive save/reload. For MVP, allow completion by returning home whether or not the player witnessed all beats. If Day3 pivotal talk was skipped, no fabricated matching-choice content: test optional fallback separately or omit the event entirely.

## F. What counts as failure (not mere aesthetic taste)

- The action looks like an NPC animation repeating or broken subtitle system.
- A label or text frames it as "rehearsal/practice/copycat" or clearly identifies an entity.
- Protagonist's replayed text is shown with `YOU` or treated as an involuntary confession.
- Every punctuation/typing bleep creates a comical glitch or high-pitched squeak.
- A loud stinger, bass drop or sudden model appears.
- A hard forced cutscene prevents player retreat.
- The scene is completely inaccessible without a hidden pixel-hunt.
- On reload, the scene restarts its first line despite already being witnessed.

## G. Playtest requirement

After each test, ask separately: `What did you think was happening?`, `Which exact moment unsettled you?`, `Did it feel like a dialogue bug?`, `Did you realize the unknown source used your own selected words?` Avoid leading participants toward the "practice" explanation. A successful scare is not simply a numerical playtime or whether they reached the door.
