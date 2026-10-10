# 08 — PERSISTENCE AND DATA-DRIVEN EVENTS

Use the existing Godot architecture after audit; below are logical contracts, not instructions to force file structures onto the game.

## Main durable state

`schema_version`, `day_index`, `time_slot`, `location`, `dialogue_choices{}`, `dialogue_exchanges[]`, `flags{}`, `npc_memories{}`, `visited_sites[]`, `observations[]`, `rehearsal_state{stage,heard_choice_1,heard_choice_2}`, `current_pc_tab`, `save_checkpoint`.

- Save `selected_text` EXACT as authored along with `choice_id` and the associated Hannah prompt+response IDs; do not assume the current line list still matches after content changes. If dialogue text changes in a future version, do a schema migration or intentionally keep stable author IDs.
- Diner day-3 choices correspond to `fri_opening` and `fri_radio`. The order is known and replayable. The player can select different choices on each new run.
- Normal conversation text labels `HANNAH`, `JUNE`, `CUSTOMER` are display labels, not speaker identity proof. `???` is strictly display-only for unknown source.
- Separate `heard_rehearsal` from `rehearsal_eligible`; do not write unobserved horror into the journal. A committed event can remain eligible later if the player walks away before the first line.
- Do not set relationship fields to arbitrary +10 numbers. A few categorical memories and facts suffice: `asked_about_film`, `met_june`, `ordered_pie`, `hannah_friendly`, `asked_june_about_door`.
- Sleep advances one and only one day. Before applying migration to existing saves, back up and create recovery paths.

## Sample data files

`data/dialogues_en.json`: authored lines, choices and replies, line_id references for exact replay. `data/events_en.json`: day and condition triggers, story state updates and transitions. `data/blip_profiles.json`: non-speech per-character synthesis profile, restrained. `data/web_pages_en.json`: short period-authored pages. `data/messages_en.json`: ordinary day-by-day instant messages. `data/qa_cases.json`: manual and automated test cases. `data/state_example.json`: initial and mid-Rehearsal state fixtures.

Scripts may adapt to a current Godot data representation, provided they preserve all semantics and can verify three things:

1. After selecting `fri_opening` choice `open_bad_day`, the `???` playback is **exactly** `Bad day?` (the same text the player clicked), not a generic response.
2. Changing choice to `open_stay_home` changes `???` playback accordingly, with no change to which day the horror unlocks.
3. Once progression reaches `rehearsal.stage=distorted`, reloading cannot reset to `initial` without explicit New Game.

## Event director policy

Checks should be explicit Boolean logic / transition rules, not random text generation. `day >= 2`, `Hannah_conversation_complete`, `hannah_exited`, `player_within_alley_area`, `rehearsal.stage not complete`. Eligibility is not "when clock shows 19:47 for 3 seconds"; no punishment for taking time. Maintain a small capped queue for captions. A pending line can be resumed after player comes back.

## Logging and debug

Developers MAY enable a local debug overlay with event flags, position, current line_id, selected_choice_ids and blip profile. Debug overlay must be off in a player build. Log missing references as errors and fall back safely without softlocking. No analytics needed for MVP unless creator opts in to local playtest event recording.
