import json
from pathlib import Path
from datetime import datetime, timezone

AUDIO_EXTS = {".wav", ".mp3", ".flac", ".m4a"}

def pick_first_audio(tracks_dir: Path):
    files = [p for p in tracks_dir.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXTS]
    files.sort(key=lambda p: p.name.lower())
    return files[0] if files else None

def main():
    root = Path(__file__).resolve().parents[1]
    config_path = root / "Config" / "free_dhu.json"
    tracks_dir = root / "Audio" / "tracks"
    beatmap_dir = root / "Audio" / "beatmap"
    beatmap_dir.mkdir(parents=True, exist_ok=True)

    with open(config_path, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)

    audio_file = pick_first_audio(tracks_dir)
    if not audio_file:
        print("ERROR: no audio file found in Audio/tracks")
        return

    beatmap = {
        "project": cfg.get("project_name", "FreeDHU"),
        "version": cfg.get("version", "1.0.0"),
        "source_audio": audio_file.name,
        "source_path": str(audio_file),
        "analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "real track linked (beat extraction pending)",
        "next": "integrate librosa beat tracking"
    }

    safe_name = audio_file.stem.replace(" ", "_")
    out = beatmap_dir / f"{safe_name}_beatmap.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(beatmap, f, indent=2)

    print("OK: beat_analyzer.py executed")
    print(f"AUDIO: {audio_file.name}")
    print(f"FILE: {out}")

if __name__ == "__main__":
    main()
