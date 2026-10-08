"""Validate the FinalRevision profile. Dependency: jsonschema."""
import json
import math
import re
import sys
from pathlib import Path


def validate(path):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        raise SystemExit("Validation requires the Python package jsonschema.")
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "references/signalforge-finalrevision.schema.json").read_text(encoding="utf-8"))
    story = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = [f"{'.'.join(map(str, e.absolute_path)) or '$'}: {e.message}"
              for e in Draft202012Validator(schema).iter_errors(story)]
    if errors:
        raise SystemExit("\n".join(errors))
    scenes = story["scenes"]
    ids = [scene["scene_id"] for scene in scenes]
    if len(ids) != len(set(ids)):
        errors.append("Scene IDs must be unique.")
    if story["runtime"]["scene_count"] != len(scenes):
        errors.append("runtime.scene_count does not match the scenes array.")
    if not math.isclose(story["runtime"]["total_seconds"], sum(s["duration_seconds"] for s in scenes), abs_tol=1e-6):
        errors.append("runtime.total_seconds does not match summed scene durations.")
    for scene in scenes:
        label = re.fullmatch(r"\*\*\s+(\d+(?:\.\d+)?)s", scene["**duration"])
        if not label or not math.isclose(float(label[1]), scene["duration_seconds"], abs_tol=1e-6):
            errors.append(f"{scene['scene_id']}: **duration must match duration_seconds.")
    if story["audio"] != story["defaults"]["audio_generation"]:
        errors.append("audio and defaults.audio_generation disagree.")
    if not story["audio"] and (story["dialogue"] or "with-audio" in story["render_settings"]["enabled"]):
        errors.append("Audio is disabled but dialogue or with-audio is enabled.")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {path} ({len(scenes)} scenes, {story['runtime']['total_seconds']} seconds)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python validate_story.py <story.json>")
    validate(Path(sys.argv[1]))
