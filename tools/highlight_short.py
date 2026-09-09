#!/usr/bin/env python3
"""
tools/highlight_short.py
========================
Cut a short highlight clip from a source video using ffmpeg.

- Preserves original source resolution (no resize)
- Applies fade=in / fade=out filters

Usage:
    python tools/highlight_short.py \\
        --input  /path/to/source.mp4 \\
        --output /path/to/highlight.mp4 \\
        --start  00:01:23 \\
        --duration 10
"""

import argparse
import subprocess
import sys


def build_ffmpeg_cmd(
    input_path: str,
    output_path: str,
    start: str,
    duration: float,
    fade_duration: float = 0.5,
) -> list[str]:
    """Return the ffmpeg argument list for cutting a clip with fades.

    No scale filter is applied — the output keeps the source resolution.
    """
    fade_out_start = max(0.0, duration - fade_duration)

    vf = (
        f"fade=in:st=0:d={fade_duration},"
        f"fade=out:st={fade_out_start}:d={fade_duration}"
    )

    return [
        "ffmpeg", "-y",
        "-ss", start,
        "-i", input_path,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path,
    ]


def cut_highlight(
    input_path: str,
    output_path: str,
    start: str,
    duration: float,
    fade_duration: float = 0.5,
) -> int:
    """Cut and fade a highlight clip. Returns ffmpeg exit code."""
    cmd = build_ffmpeg_cmd(input_path, output_path, start, duration, fade_duration)
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd).returncode


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cut a highlight short from a source video."
    )
    parser.add_argument("--input",    required=True,              help="Source video path")
    parser.add_argument("--output",   required=True,              help="Output clip path")
    parser.add_argument("--start",    required=True,              help="Start timecode (HH:MM:SS or seconds)")
    parser.add_argument("--duration", required=True, type=float,  help="Clip duration in seconds")
    parser.add_argument("--fade",     default=0.5,  type=float,   help="Fade duration in seconds (default: 0.5)")
    args = parser.parse_args()

    sys.exit(cut_highlight(args.input, args.output, args.start, args.duration, args.fade))


if __name__ == "__main__":
    main()
