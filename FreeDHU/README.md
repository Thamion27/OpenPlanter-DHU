# FreeDHU v1.0 Runbook

## Location
C:\Users\rrami\OpenPlanter\FreeDHU

## Restart Rhythm
1. cd C:\Users\rrami\OpenPlanter
2. .\.venv\Scripts\Activate.ps1
3. cd .\FreeDHU

## Pipeline Commands
python .\Scripts\beat_analyzer.py
python .\Scripts\scene_builder.py
python .\Scripts\sync_engine.py
python .\Scripts\run_pipeline.py

## Render Test
ffmpeg -y -f lavfi -i color=c=black:s=1920x1080:r=30:d=60 -i ".\Audio\tracks\Relentless Vision (1).wav" -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac ".\Output\renders\demo_render.mp4"

## Current Milestone
Tag: freedhu-v1.0-scaffold
Commit: c280581
