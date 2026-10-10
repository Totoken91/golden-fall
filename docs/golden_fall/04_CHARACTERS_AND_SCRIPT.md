# 04 — CHARACTERS AND SCRIPT TONE

These are implementation targets and drafts in natural US English, not an instruction to flood the game with dialogue. The characters must feel like ordinary residents who did not wait for the player to exist.

## June Mercer — diner worker (early 20s, age provisional)

Practical, dry, somewhat tired, not a joke dispenser. Knows customers' habits; has work to do. She can be kind without acting like a game tutorial. Physical model: simple recognizable apron, dark undershirt, hair tied back or short, minimal head/arm movement, no exaggerated facial expressions. Keep her visible doing something mundane at counter; don't make her orbit/track protagonist constantly.

Day 1:
- `JUNE`: `Coffee's fresh. Pie's been here since noon.`
- Choices: `Just coffee, thanks.` / `Is the pie that bad?` / `I'll look around first.`
- Choice 2 response: `It's fine. Just don't ask what time we made it.`
- Choice 3 response: `Sure. Just keep the door shut. It's cold out.`

Day 2 (conditional if bought pie): `You survived the pie. I'll put that on the sign outside.`
Day 2 (if never spoke): `You were in here yesterday, right?` (not an impossible claim; she's attentive)
Day 3: she may say `Hannah's over by the window if you're looking for her.` This should sound contextual, not a glowing map waypoint. If player asks about service door after event: `That door sticks. It barely opens for deliveries.` and, after player mentions a voice, `I didn't see her out back. I was in the kitchen.` Nothing confirms or denies.

## Hannah Vale — student / analog photography hobbyist (late teens, age provisional)

Photography interest exists for mundane reasons. Unpolished teen personality: somewhat guarded with strangers, dry humor, occasionally self-conscious. Not a 'quirky mysterious girl', not a designated quest vendor. Low-poly outfit: worn olive jacket, dark sweater, thrift-store skirt or jeans (confirm before art lock), camera strap as recognizable silhouette. Gesture economy: look toward window, rest hands on prints, brief head turn, straighten coat while leaving. No mouth animation, skeletal face detail or 2D portrait.

Day 1:
- `HANNAH`: `You can sit there. Just don't put your elbow on the prints.`
- Choices: `Those yours?` / `Sorry.` / `Any good ones?`
- Replies: `Yeah. Most of them look like the inside of a toaster.` / `You're fine. I keep spreading them everywhere.` / `Maybe two. I'm keeping the bad ones anyway.`

Day 2 follows up from exact Day1 topic if encountered; otherwise a clean introduction. Do not grant relational advancement simply for exhausting options. Optional mundane beat: she took a photo through diner window but rain ruined it; no face hidden in it, no spooky Easter egg.

Day 3 memorable natural conversation with TWO player choice points; these exact lines fuel The Rehearsal:

`HANNAH`: `I almost didn't come tonight.`
Response A: `Bad day?`
- `HANNAH`: `Nothing dramatic. I just kept putting my shoes on and taking them off.`
Response B: `You could've stayed home.`
- `HANNAH`: `I know. That's why I came.`
Response C: `I'm glad you did.`
- `HANNAH`: `...Yeah. Me too.`

Then, after some ordinary pause and a movement to window:
`HANNAH`: `June turns the radio down when it rains.`
Response A: `Maybe she likes the sound.`
- `HANNAH`: `Could be. This roof makes enough noise for both of us.`
Response B: `I hadn't noticed.`
- `HANNAH`: `You will now.`
Response C: `Isn't that backwards?`
- `HANNAH`: `Probably. Ask her. She never gives me the same answer.`

She leaves because she has an ordinary ride or early errand tomorrow, not because she senses the horror. Goodbye variant if player has spoken kindly: `See you around.` Else `Night.` Avoid a knowingly cryptic closing line.

## Protagonist: first person, no name label in dialogue by default

Choices are the protagonist's spoken responses in normal face-to-face dialogue, but no `YOU:` boxed speaker label is necessary. During The Rehearsal, the exact selected words appear under `???`, never under protagonist speaker ID. No offscreen internal monologue interpreting events. The player should recognize their decision without being told it is happening.

## Ordinary overheard dialogue: teach convention

Day 1 ambient inside diner while player away from counter:
`JUNE`: `Could you grab the door for me? My hands are full.`
`CUSTOMER`: `Got it.`
This is not supernatural. Day 2 normal offscreen line should teach that subtitles can appear while the source is outside the camera's field of view. Timing/blips conform exactly to horror version (except horror's authored timing irregularity).

## Character ethics and style

Never reduce Hannah to a rescue objective or source of mystery exposition. June has shifts and irritations independent of protagonist. People's reactions should be proportionate and realistic. Avoid rapid intimacy in three days and don't promise romance as a mechanical reward. No uncanny facial-expression requirement: pauses, head angles, clothing and natural American speech do the work.

## Rehearsal line-data fidelity

All live conversation lines have stable `line_id`s, and the player choice has stable `choice_id`. Runtime stores `{node_id, choice_id, selected_text, hannah_reply_id, hannah_reply_text}`; display uses the authored text. Rehearsal references same underlying stored text, not a second manually typed string that could drift. It must work for all nine combinations of the two choice points.
