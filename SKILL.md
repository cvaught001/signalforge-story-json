---
name: signalforge-story-json
description: Create or revise SignalForge story JSON in the FinalRevision_v1.14 format, with Markdown scene locks, character-file links, image references, runtime metadata, and editor render settings. Use for SignalForge JSON story requests rather than standalone Markdown stories.
---

# SignalForge story JSON

Create a complete UTF-8 `.json` story in the format demonstrated by `apps/SignalForge/stories/FinalRevision_v1.14.json`. These instructions and bundled resources work with Claude and Codex; they require no provider-specific tools.

Read [the format guide](references/format.md) and [the neutral template](assets/story-template.json). Consult [the JSON Schema](references/signalforge-finalrevision.schema.json) only for uncertain field types or validation errors; the validator loads it automatically. Resolve paths relative to this skill folder. The bundle is self-contained; access to the original example is optional.

## Select the workflow

For an existing Markdown storyboard, use direct conversion below. For a new story idea, use the authoring guidance. Do not search for the original FinalRevision story, other skills, asset collections, or backend documentation just to convert supplied text. External MiniMax review applies only when requested; this bundle does not currently contain an authoritative MiniMax skill.

### Direct conversion

1. Extract metadata, global rules, and scenes in one pass. Preserve titles, order, explicit durations, reference descriptions, visual prompts, audio instructions, dialogue, and speaker IDs. Preserve `<d speaker="host_01">...</d>` tags inside strings; they convey speaker intent but do not guarantee backend voice identity.
2. Populate the template envelope. Map global and character rules into `global_style`, `story_continuity`, and `negative_prompt`. Keep each existing scene's Markdown in `scene`, including its original headings. The expanded locks below are for newly authored scenes; conversion does not require rewriting a detailed storyboard into all nine sections. Populate `subjects` from visible characters; an off-camera narrator is not a visible subject. Copy descriptive references into `**references`. Leave actual reference arrays empty without supplied paths, set `image_conditioning` to false, and report that images still need attaching.
3. Treat explicit scene durations as the default source of truth. If their sum conflicts with a header target, preserve the scenes and report both durations. Do not silently shorten dialogue, retime scenes, or loop on competing constraints. Adapt to the target only when explicitly requested. Set nominal `seconds_per_scene` to the most common supplied duration; calculate count and total from actual scenes.
4. Preserve dialogue verbatim. Perform one brief pacing review and flag likely overlong lines without rewriting unless requested. A rough 120–150 words/minute estimate is a planning heuristic for measured narration, not a MiniMax limit or proof of actual delivery time. Scope historical period restrictions to reenactments when the script explicitly includes a present-day host; preserve the host's supplied wardrobe.
5. Serialize once, validate once, and fix concrete validation errors. Deliver the JSON and a short list of unresolved input conflicts. Do not render, install tooling, or repeat stylistic reviews during conversion. When tools are unavailable, return complete JSON and say automated validation was unavailable.

Use a supplied profile/workflow when available. Otherwise leave `model-workflow` unset and disabled rather than searching for or asserting a verified backend. Missing assets or backend configuration do not block producing JSON.

## Authoring

- Establish the requested story beats, cast identities, duration, aspect ratio, visual style, dialogue, sound, and supplied assets. Infer reasonable creative details when unspecified; ask only about missing information that materially affects the result. Preserve supplied beats and dialogue.
- Start from the neutral template. Keep its field names, nesting, and JSON types, including the unusual `**references` and `**duration` keys. Replace template content with the requested story. The source's Halloween plot, eight-scene count, audio restrictions, and 9:16 framing are examples, not universal creative rules.
- Keep `schema: "signalforge.story"`, `schema_version: "1.0"`, and `format: "signal-forge-markdown"`. `version` is the story revision, not the schema version. Point `$schema` to the bundled format schema using a path relative to the output file; do not claim conformance to the project's shared schema without checking it.
- Write unique sequential IDs (`scene_01`, `scene_02`, ...), informative titles, and positive durations. Keep scenes in narrative order. Set `runtime.scene_count` to the actual count and `runtime.total_seconds` to the sum. `seconds_per_scene` is the nominal duration; individual scenes may differ.
- Write each `scene` as one Markdown string using the locks in the format guide. Describe cast counts, stable character identities, framing, ordered action, sound, exact dialogue and speaker, continuity, and exclusions. Fit action and dialogue into the shot duration. Repeat identity-critical details where scenes must stand alone; use names rather than ambiguous pronouns.
- Keep `subjects` aligned with visible cast and action. Use consistent character IDs. Link `character_locks` to supplied character JSON files; do not invent existing files. Without files, use an empty map and put complete identities in the scene strings. Extras may be described in `subjects` without a character-file link.
- Keep actual image conditioning in `image_refs.references` and environmental images in `environment_lock.references`. The `**references` string describes intent and does not load assets. Leave arrays empty when no files were supplied. Never invent reference paths. Match audio flags, dialogue flags, visible-text settings, scene instructions, and render options to one another.
- Keep render setting values as strings and use existing configuration when available. Do not inherit the source's partial render range (`start: "5"`, `end: "8"`) for a new full story. Choose a verified workflow for the requested backend; the template workflow is an example configuration, not a guarantee that it is installed.

## Check and deliver

When Python and `jsonschema` are available, run:

```sh
python scripts/validate_story.py /path/to/story.json
```

Run from this skill folder or use the script's absolute path. The validator checks the bundled format schema, IDs, runtime totals, duration labels, and basic audio flag consistency. Install `jsonschema` only within the user's environment and authorization, or report that automated validation was unavailable. Also review identity, blocking, prop state, sound, dialogue, asset paths, and pacing manually; structural validation cannot prove those.

With filesystem access, save a new story in the requested location (normally `apps/SignalForge/stories/<title>.json`) and report its path and validation result. Preserve unknown fields when revising an existing story. Without filesystem access, return one complete JSON code block without comments, trailing commas, omitted scenes, or ellipses. Generate the story file; rendering is a separate user request.
