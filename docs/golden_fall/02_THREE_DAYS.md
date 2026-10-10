# 02 — THREE DAYS, SPATIAL AND NARRATIVE BEAT SHEET

The player can roam freely. Times below are scene targets, not literal real-time wait requirements. **Do not auto-teleport into conversations**. English-only player presentation.

## DAY 1 — WEDNESDAY, OCT 15 — "The window seat" (~7–12 min)

**Room / 16:10.** Existing bed and PC; rainfall against glass, a little desk-lamp warmth. An unread IM on the PC from a class acquaintance (username `mossline`): "June's got the late shift. Diner's open if you need somewhere dry." This is optional. Player can look at rain, inspect a record, save and leave. Nothing calls itself an objective.

**Street.** 60–100m of walkable golden-fall town; limited but layered horizon with dark woods. Diner visible by light and composition, not an enormous floating quest marker. At least one pedestrian silhouette/parked car is set dressing, not a dialogue-rich extra. Need believable sidewalk collisions and wet-ground footsteps.

**Diner.** June handles the counter with practiced pragmatism. Hannah sits near the window sorting badly exposed photographs. The player can order a drink, listen to ambience, talk to June and Hannah, or leave. June asks a simple question and remembers the answer; Hannah can be approached and offers a plausible conversation about film and town light. No prophecy, supernatural teaser or talk of the forest from every NPC. No mechanical trust bar.

**End.** Player can walk home, use PC, sleep. If no one was approached, next day still begins; do not award fake 'friendship'. One incidental offscreen subtitle from a normal customer/June exchange introduces the **same text grammar** later used in The Rehearsal.

## DAY 2 — THURSDAY, OCT 16 — "A place that feels lived in" (~7–12 min)

**Room.** PC IM or bulletin board can present something mundane: a lost jacket, a failed gig flyer, a diner menu joke. A Web search for `Morrow Creek` yields school newsletter / Morrow paper / old music page; two pages are useful worldbuilding, neither is a required clue.

**Street and diner.** Lighting subtly different (gray daylight vs amber rain). June recognizes greeting history if seen before; otherwise normal first meeting. Hannah can discuss a photo she nearly threw away. If player asked about film on Day1, she alludes to it; else answers without pretending to remember. Player sees/inspects a non-expository diner artifact, e.g. a dated contact sheet or small band flyer. Let this be human and ordinary.

**Offscreen dialogue convention:** June says a short line to a customer while player is NOT looking at either source. The game shows unobtrusive `JUNE` text and natural blips in response. It's crucial that viewers learn this is a normal UI behavior before Day3. A small alternative customer text can appear as `CUSTOMER` without any ghost implication.

**End.** Sleep if ready. No mandatory anomalous vignette. Mood and attachment must hold their own.

## DAY 3 — FRIDAY, OCT 17 — "The same words" (~10–20 min)

**Room / late afternoon.** Optional normal IM about rainy weather and diner hours. The player can walk around town, then enter diner; ordinary customers are leaving. June is finishing service. Hannah sits by the familiar window. Critical conversation is available through interaction: two distinct choice points with **exact selected response text** stored by ID and string.

**Pivotal conversation** (all playable English dialogue in `data/dialogues_en.json`): Hannah discusses almost not coming tonight and the way June lowers the radio when it rains. These lines must be delivered as believable friendly small talk, *not foreboding speeches*. Her exit follows naturally (collects coat/camera, steps out front). Player can talk briefly with June, pay, linger, leave.

**Alley entrance.** The rear/service walkway is reachable from the street; warm window light gives way to a trash bin, wet brick, an exhaust fan, a shut service door. From just beyond a corner, on-screen OFFSCREEN dialogue starts: `HANNAH` line exactly quoted from the dialogue just had. At first it could simply be Hannah on the other side of the building. The next text is EXACTLY the selected player response, now labeled `???`. Not `YOU`. Not a metaphor. This is when the player can recognize the impossibility.

**Disturbance:** fragments of Hannah's same line occur with unnatural punctuation, mid-word rests and rhythm changes; the text UI retains natural appearance. Part of an `???` fragment may repeat a word from Hannah. Do not imply a mechanism (no dialog about practice/learning). The sequence is responsive to player presence but not mechanically "when you step closer, the creature learns"; leave space for hesitation and exploration.

**Aftermath:** Player can try the service door (physically secured), return for June (short uncertain response, she doesn't diagnose), leave or return to listen. No creature, battle or loud climax. Room feels familiar again, which is now uncomfortable. Sleep/neutral `End of this prototype` after voluntary return; optionally an ordinary IM is present, not a second horror twist.

## Optional and mandatory distinctions

**Mandatory to finish micro-MVP:** room→outside traversal, ability to sleep through 3 days, return path home, save/load. **Mandatory to validate core intended horror route:** meet Hannah at least on Friday, complete her two choice points, find service alley and see selected-response replay. **Not mandatory on every player's playthrough:** listening all the way, exploring PC, contacting June, return to diner on Day2. Never misrepresent route content in the journal when skipped.

## Authoring constraint

The intro must NOT mention missing brother Evan as the central hook and must not show the 1998 photograph. Those are reserved future mysteries. The first nightmare-worthy intrusion here comes from an ordinary line heard out of context, not new lore.
