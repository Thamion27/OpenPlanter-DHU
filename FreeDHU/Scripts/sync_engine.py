import json
from pathlib import Path
from datetime import datetime, timezone

def main():
    root = Path(__file__).resolve().parents[1]
    timeline_path = root / "Output" / "metadata" / "demo_timeline.json"
    metadata_dir = root / "Output" / "metadata"
    logs_dir = root / "Output" / "logs"
    renders_dir = root / "Output" / "renders"
    tracks_dir = root / "Audio" / "tracks"

    metadata_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)

    with open(timeline_path, "r", encoding="utf-8-sig") as f:
        timeline = json.load(f)

    source_audio_name = timeline.get("source_audio", "")
    source_audio_path = tracks_dir / source_audio_name if source_audio_name else None
    audio_exists = bool(source_audio_path and source_audio_path.exists())

    scenes = timeline.get("scenes", [])
    total_duration = 0
    if scenes:
        total_duration = max(s.get("end_sec", 0) for s in scenes)

    render_plan = {
        "project": timeline.get("project", "FreeDHU"),
        "version": timeline.get("version", "1.0.0"),
        "status": "sync engine linked to real timeline/audio",
        "source_audio": source_audio_name,
        "source_audio_path": str(source_audio_path) if source_audio_path else "",
        "source_audio_exists": audio_exists,
        "source_beatmap": timeline.get("source_beatmap", ""),
        "scene_count": len(scenes),
        "estimated_duration_sec": total_duration,
        "target_output": str(renders_dir / "demo_render.mp4"),
        "next": "integrate ffmpeg render pass"
    }

    out = metadata_dir / "demo_render_plan.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(render_plan, f, indent=2)

    log_file = logs_dir / "sync_engine.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} - sync_engine linked real audio\n")

    print("OK: sync_engine.py executed")
    print(f"FILE: {out}")
    print(f"FILE: {log_file}")

if __name__ == "__main__":
    main()
