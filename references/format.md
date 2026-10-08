# FinalRevision JSON format

This profile derives from `apps/SignalForge/stories/FinalRevision_v1.14.json`. It preserves that file's data layout while allowing other stories. The bundled schema describes this profile, not every format supported by SignalForge.

## Top level

The neutral template includes every top-level field in the reference: `$schema`, `schema`, `schema_version`, `project_title`, `format`, `version`, `aspect_ratio`, `defaults`, `negative_prompt`, `audio`, `global_style`, `scenes`, `character_locks`, `studio`, `model`, `tone`, `dialogue`, `story_continuity`, `runtime`, and `render_settings`.

- `audio` and `dialogue` are booleans. `defaults` contains `prompt_compilation_mode`, `image_conditioning`, `allow_visible_text`, `audio_generation`, `image_strength`, and `image_crf`.
- `global_style` contains string fields `description`, `photographic_style`, `lighting`, and `mood`, plus a string array `color_palette`.
- `character_locks` maps stable character IDs to objects such as `{"character_file": "Character.json"}`. Use only supplied or verified files; an empty map is valid for a self-contained prompt story.
- `story_continuity` gives ordered beats and persistent character, prop, location, reference-priority, and sound rules. Prefer explicit scene-specific exceptions over contradictory blanket rules.
- `runtime` contains numeric `scene_count`, `total_seconds`, and `seconds_per_scene`. The source has durations 7/7/7/7/7/7/12/15 (69 seconds); its nominal duration is 7. Do not calculate total duration by multiplying the nominal value by scene count.
- `render_settings.enabled` is a string array of selected editor option names. `values` maps option names to strings, including numbers represented as strings and empty strings for unset controls. Enable only applicable options; audio-disabled stories must not enable `with-audio`.

## Scene fields

Each scene uses `scene_id`, `title`, `duration_seconds`, `scene`, `image_refs`, `**references`, `**duration`, `environment_lock`, and `subjects`.

Use the following sections inside the `scene` string, separated by blank lines. JSON serializes newlines as `\n`; use a JSON serializer when possible rather than manually escaping text.

```text
**storyboard_lock:** Supplied panel/beat and what it controls; otherwise the intended story beat.

**cast_lock:** Exact visible people, counts, and screen positions; explicitly identify extras.

**character_priority:** Identity, silhouette, wardrobe, behavior, and separation of named characters.

**portrait_composition:** Aspect ratio, foreground/midground/background, lens feel, camera movement, and framing. For nonportrait stories describe the chosen framing under this compatibility heading.

**action:** A chronological, physically plausible action sequence for one shot.

**audio:** Allowed sound, ambience, effects, music, voice qualities, and explicit silence where needed.

**dialogue:** Exact words and speaker, on/off-camera delivery, mouth synchronization, and silent characters.

**continuity:** Starting/ending state, persistent props, locations, and character placement.

**negative:** Scene-specific exclusions consistent with the global rules.

---
```

`**references` is a string beginning with `** ` that describes reference intent. `**duration` is a string such as `** 7s` matching the numeric duration. These odd keys are retained for compatibility with the example.

`subjects` is an array of objects containing `character`, `description`, and `action`. Use an empty array for a shot with no characters. Crowd subjects describe the count and distinguish extras from leads.

`image_refs` and `environment_lock` each contain `references`, initially `[]`. With verified assets, reference entries may be strings or objects with `image`, plus optional `label`, `description`, `role`, `frame_idx`, `strength`, and `crf`. Environment entries use objects. Character reference identity, storyboard action, and prop design should have clearly separated authority.

## Compatibility limits

The project's `schemas/signalforge-story-1.0.schema.json` currently requires top-level `audio` to be an object, whereas this source has `audio: true`. The bundled schema intentionally accepts the source's boolean. Do not alter the source or shared schema just to create this skill.

`scripts/validate_signalforge_story.py` validates a different, expanded `SignalForge_FLUX_JSON` layout. Use this skill's validator for this profile; do not add unrelated required FLUX fields such as `final_prompt` to appease that validator.

Schema conformance does not prove render readiness. Character-file links, references, backend workflow, credentials, and profiles must exist in the destination environment before rendering.
