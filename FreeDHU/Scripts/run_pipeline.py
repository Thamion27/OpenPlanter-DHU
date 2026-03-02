import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

def run_step(script_path):
    r = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    return {
        "script": script_path.name,
        "returncode": r.returncode,
        "stdout": r.stdout.strip(),
        "stderr": r.stderr.strip()
    }

def main():
    root = Path(__file__).resolve().parents[1]
    scripts_dir = root / "Scripts"
    metadata_dir = root / "Output" / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    steps = [
        scripts_dir / "beat_analyzer.py",
        scripts_dir / "scene_builder.py",
        scripts_dir / "sync_engine.py",
    ]

    results = [run_step(s) for s in steps]
    ok = all(x["returncode"] == 0 for x in results)

    status = {
        "project": "FreeDHU",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": "ok" if ok else "failed",
        "steps": results
    }

    out = metadata_dir / "pipeline_status.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)

    print("OK: run_pipeline.py executed")
    print(f"FILE: {out}")
    for s in results:
        print(f"- {s['script']}: rc={s['returncode']}")

if __name__ == "__main__":
    main()
