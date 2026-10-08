# BETA -SignalForge Story JSON Skill

A portable Claude and Codex skill for creating SignalForge story JSON in the format of `FinalRevision_v1.14.json`.

Includes Markdown scene locks, character-file links, image-reference arrays, runtime metadata, editor render settings, a neutral story template, and a JSON Schema specific to this format.

## Use with Claude Code

Clone this repository into your project's `.claude/skills/signalforge-story-json` directory, or into `~/.claude/skills/signalforge-story-json` for personal use. Invoke:

```text
/signalforge-story-json Create a 30-second cinematic story about a lantern keeper.
```

For a Claude interface that accepts skill uploads, upload a ZIP containing the `signalforge-story-json/` folder with `SKILL.md` and its supporting files.

## Use with Codex

Place the skill folder under `~/.codex/skills/signalforge-story-json`, or ask Codex to read `SKILL.md` directly. Invoke `$signalforge-story-json` with your story request when installed.

## Validate a story

Requires Python 3 and `jsonschema`. From the repository directory:

```sh
python -m pip install -r requirements.txt
python scripts/validate_story.py assets/story-template.json
python scripts/validate_story.py /path/to/story.json
```

Validation checks structure, unique scene IDs, runtime totals, duration labels, and basic audio flags. Review pacing, continuity, and asset availability separately.

## Format compatibility

Read [SKILL.md](SKILL.md) for authoring instructions and [references/format.md](references/format.md) for field details. The [bundled schema](references/signalforge-finalrevision.schema.json) preserves boolean top-level `audio` from the reference story; SignalForge's shared schema currently expects an audio object. The original story and shared schema are not modified by this skill.

The [neutral template](assets/story-template.json) contains no private reference images or character assets. Renderer profiles and backend workflows must be available in the destination environment. This skill creates story JSON; it does not render video.
