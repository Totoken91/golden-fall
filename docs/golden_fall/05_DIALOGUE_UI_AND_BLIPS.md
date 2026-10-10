# 05 — FPS DIALOGUE UI, AMBIENT TEXT, AND SOUND BLEEPS

## Basic UI

No portrait overlays. Very low-poly characters remain in world; text boxes occupy the bottom quarter or less of view on desktop (adaptive to resolution). A simple name tag in small caps (`HANNAH`, `JUNE`, `CUSTOMER`, `???`), cream-white type, muted translucent coffee-black background. Avoid fantasy-gothic ornaments; favor quiet early-2000s typography, readable with rough retro rendering. Dialogue can be advanced with keyboard/mouse; choices with keyboard/scroll/click. Input mode must release mouse appropriately and restore FPS input reliably when closed. Never move the player's character to a magic cinematic mark solely to show a text panel.

## Typewriter pacing

Default readable typing ~32–45 characters/sec adjustable to player's preference; a player setting offers instant full-line reveal. Do NOT tie story duration to typing speed. Pauses after punctuation but skip/advance should remain responsive. For accessibility, provide `Text speed`, `Text bleeps: on/off`, `Text bleep volume`, `Subtitle persistence / last lines` and reasonable fallback for hearing-impaired players. Blips don't convey required information that text alone cannot.

## Character blips

Think Animal Crossing's concept of identifying speakers via tiny note-like sounds, but **less goofy and not pretending to pronounce actual English**. Procedural short, warm, nonverbal bleeps only: sine/triangle-like, lowpassed, rounded ADSR, very low gain, gentle pitch range. In the prototype, synthesize in-engine or use original one-shot samples; no copyrighted game samples. Restrained per-character palette:

- Hannah: slightly low, mellow, rounded, modest variation and unhurried spacing.
- June: a touch brighter/drier and brisker, still subdued.
- Customer: quiet neutral pulse.
- `???`: ambiguous, almost normal. Do NOT choose a villain noise or distorted demon voice; occasionally borrow another profile only if clearly tested. `???` remains unknown regardless of timbre.

Trigger blips on text grapheme clusters or e.g. every second printable character with throttling around **5–9 notes/sec max**; do not trigger on spaces, line breaks or every repeated punctuation mark. Add slight deterministic variation; do not add random sharp transients. Options to disable without losing information. Ensure no overlapping bursts when player skips full line.

### Implementation guide (not mandated code)

Godot: `DialoguePresenter` and `TextBleepPlayer` components should reuse a single unified speaker/text event. Keep speaker blips separate from ambient 3D layers; subtitle text is a narrative UI convention while the sound blip is UI-local—not a physical source you can surround-sound triangulate like a recorded voice. Spatial relevance controls *whether* an offscreen line can be received. Test mono playback and headsets.

## Three dialogue channels

1. **Focused** face-to-face: interaction opens bottom panel and 1–3 textual responses; player can look slightly around and close when done. Character still performs low-cost idle.
2. **Ambient/offscreen**: line appears near bottom of FPS view when within a credible hearing/awareness zone; no choices, player moves freely. Tags/bleeps as usual. Establish BEFORE horror.
3. **Anomalous offscreen**: visually the same as ambient, but runtime stages exact earlier lines, selected response under `???`, pauses and deliberate fragments. No red labels, corrupted fonts, letter scrambling, rapid screen shakes or horror UI styling.

### UX when player moves

Offscreen captions should not fire continuously while player re-crosses a trigger. Use a stateful transcript queue: eligibility, pending, printed, consumed. Keep an easily accessible last-caption buffer of roughly 3–5 lines for readers who looked away; do NOT auto-explain the anomaly in that log. A proximity threshold changes eligibility, not resets. If the player moves away mid-caption, finish current readable line before fading, unless it is an authored sudden interruption.

## Very low-poly bodily expressiveness

For both NPCs, prioritize 1 idle seated pose, 1 standing pose, head tilt, look away, hand movement with print/mug, modest shoulder turn. Avoid complex lip rigs and uncanny baked facial expressions. Their faces can be almost unreadable; writing and body arrangement fill in the gaps.
