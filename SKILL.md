---
name: signalforge-story-json
description: Create or revise SignalForge story JSON in the FinalRevision_v1.14 format, with Markdown scene locks, character-file links, image references, runtime metadata, and editor render settings. Use for SignalForge JSON story requests rather than standalone Markdown stories.
---

# SignalForge story JSON

Create a complete UTF-8 `.json` story in the format demonstrated by `apps/SignalForge/stories/FinalRevision_v1.14.json`. These instructions and bundled resources work with Claude and Codex; they require no provider-specific tools.

Read [the format guide](references/format.md), [the JSON Schema](references/signalforge-finalrevision.schema.json), and [the neutral template](assets/story-template.json) before creating a story. Resolve these paths relative to this skill folder. The bundle is self-contained; access to the original example is optional.

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
