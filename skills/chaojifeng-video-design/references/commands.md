# 常用查询与检查

将 SKILL_ROOT 替换为本 Skill 根目录。选项以脚本 --help 为准；检查不代替实际制作、观看和试听。

```text
python3 SKILL_ROOT/scripts/catalog.py --kind scenario list
python3 SKILL_ROOT/scripts/catalog.py --kind style list
python3 SKILL_ROOT/scripts/catalog.py --kind motion get reveal
python3 SKILL_ROOT/scripts/catalog.py --kind expression list --scenario brand-film
python3 SKILL_ROOT/scripts/catalog.py --kind expression get visual.target-callout
python3 SKILL_ROOT/scripts/catalog.py --kind recipe list --scenario music-visual
python3 SKILL_ROOT/scripts/catalog.py --kind recipe get product-task-proof
python3 SKILL_ROOT/scripts/production_tools.py list --task environment
python3 SKILL_ROOT/scripts/production_tools.py probe
python3 SKILL_ROOT/scripts/production_tools.py polyhaven-search --query studio --type hdris --limit 5 --cache-dir /project/video/cache/polyhaven
python3 SKILL_ROOT/scripts/production_tools.py aivis-speakers
python3 SKILL_ROOT/scripts/production_tools.py check /project/video/production-job.json --require-reviewed
python3 SKILL_ROOT/scripts/music_library.py search --scenario product-demo --emotion curious --role establish --avoid-bright --limit 5
python3 SKILL_ROOT/scripts/music_library.py select --recipe knowledge-music-explainer
python3 SKILL_ROOT/scripts/music_library.py select --recipe knowledge-music-explainer --source-file /project/music/chosen.wav
python3 SKILL_ROOT/scripts/validate_plan.py /project/video/plan.json
python3 SKILL_ROOT/scripts/knowledge_pack.py /project/video/plan.json
python3 SKILL_ROOT/scripts/controlled_lint.py --text-file /project/video/script.txt --profile ste-zh-spoken --glossary /project/video/plan.json
python3 SKILL_ROOT/scripts/check_delivery.py /project/video/plan.json /project/video/delivery.json --probe --require-video
python3 SKILL_ROOT/scripts/film_probe.py /path/to/film.mp4 --out /project/video/probe.json --frames-dir /project/video/probe-frames
python3 SKILL_ROOT/scripts/audio_event_audit.py /project/video/audio-event-map.json /project/video/sfx-stem.wav --out /project/video/audit.json
python3 SKILL_ROOT/scripts/explainer_timing_audit.py /project/video/knowledge-music-score.json --plan /project/video/plan.json --music-sheet /project/video/music-cue-sheet.json
```
