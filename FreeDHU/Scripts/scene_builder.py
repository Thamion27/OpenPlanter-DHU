import json
from pathlib import Path
from datetime import datetime, timezone

def pick_beatmap(beatmap_dir: Path):
    # prefer non-demo beatmaps
    files = [p for p in beatmap_dir.glob("*_beatmap.json") if "demo" not in p.name.lower()]
    if not files:
        files = list(beatmap_dir.glob("*.json"))
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def main():
    root = Path(__file__).resolve().parents[1]
    beatmap_dir = root / "Audio" / "beatmap"
    metadata_dir = root / "Output" / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    beatmap_file = pick_beatmap(beatmap_dir)
    if not beatmap_file:
        print("ERROR: no beatmap json found in Audio/beatmap")
        return

    with open(beatmap_file, "r", encoding="utf-8-sig") as f:
        beatmap = json.load(f)

    timeline = {
        "project": beatmap.get("project", "FreeDHU"),
        "version": beatmap.get("version", "1.0.0"),
        "source_audio": beatmap.get("source_audio", "unknown"),
        "source_beatmap": beatmap_file.name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scenes": [
            {"id": 1, "start_sec": 0,  "end_sec": 10, "type": "intro"},
            {"id": 2, "start_sec": 10, "end_sec": 30, "type": "main"},
            {"id": 3, "start_sec": 30, "end_sec": 45, "type": "bridge"},
            {"id": 4, "start_sec": 45, "end_sec": 60, "type": "outro"}
        ],
        "status": "scene builder linked to real beatmap",
        "next": "integrate beat-driven segmentation"
    }

    out = metadata_dir / "demo_timeline.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2)

    print("OK: scene_builder.py executed")
    print(f"BEATMAP: {beatmap_file.name}")
    print(f"FILE: {out}")

if __name__ == "__main__":
    main()
