"""
ReelPipeline — automatically extract short-form vertical reels from a long video.

Usage:
    from apps.signal_loom.pipelines.reel_pipeline import ReelPipeline

    pipeline = ReelPipeline(account='studio__73', platform='instagram', vertical=True)
    result = pipeline.run(
        source_video='/path/to/long_video.mp4',
        output_dir='/path/to/reels/',
        top_n=5,
    )
    print(result)

Dependencies:
    pip install moviepy numpy
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Platform configuration
# ---------------------------------------------------------------------------

PLATFORM_CONFIG: dict[str, dict] = {
    "instagram": {
        "aspect_ratio": (9, 16),
        "min_duration": 3,
        "max_duration": 90,
        "target_duration": 30,
        "fps": 30,
        "resolution": (1080, 1920),
    },
    "tiktok": {
        "aspect_ratio": (9, 16),
        "min_duration": 5,
        "max_duration": 600,
        "target_duration": 30,
        "fps": 30,
        "resolution": (1080, 1920),
    },
    "youtube_shorts": {
        "aspect_ratio": (9, 16),
        "min_duration": 5,
        "max_duration": 60,
        "target_duration": 30,
        "fps": 30,
        "resolution": (1080, 1920),
    },
}


# ---------------------------------------------------------------------------
# Result data classes
# ---------------------------------------------------------------------------

@dataclass
class ReelClip:
    """Metadata for a single exported reel clip."""
    path: str
    start_time: float
    end_time: float
    duration: float
    score: float
    rank: int

    def __repr__(self) -> str:
        return (
            f"ReelClip(rank={self.rank}, score={self.score:.4f}, "
            f"time={self.start_time:.1f}s-{self.end_time:.1f}s, "
            f"file={Path(self.path).name})"
        )


@dataclass
class ReelResult:
    """Aggregate result returned by :meth:`ReelPipeline.run`."""
    source_video: str
    output_dir: str
    account: str
    platform: str
    reels: list[ReelClip] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"ReelResult(account={self.account!r}, platform={self.platform!r}, "
            f"source={Path(self.source_video).name!r}, reels={len(self.reels)})"
        )


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class ReelPipeline:
    """
    Pipeline for extracting the top-N most engaging short clips from a long
    source video and exporting them as platform-ready vertical reels.

    Scoring strategy
    ----------------
    The default scorer is ``'audio_energy'``: each candidate window is ranked
    by its mean RMS audio level.  This is fast, dependency-free (only numpy is
    needed), and works well for interview / talking-head footage.

    Args:
        account:           Identifier for the social media account (used in
                           output filenames).
        platform:          Target platform — ``'instagram'``, ``'tiktok'``, or
                           ``'youtube_shorts'``.
        vertical:          When *True* the clip is center-cropped to the
                           platform's 9:16 aspect ratio.
        segment_duration:  Duration (seconds) of each candidate window.
                           Defaults to the platform's ``target_duration``.
        overlap:           Fraction of ``segment_duration`` used as the sliding
                           step (0 < overlap < 1).  0.5 means 50 % overlap.
        scorer:            Scoring strategy.  Currently only ``'audio_energy'``
                           is supported.
    """

    def __init__(
        self,
        account: str,
        platform: str = "instagram",
        vertical: bool = True,
        segment_duration: Optional[float] = None,
        overlap: float = 0.5,
        scorer: str = "audio_energy",
    ) -> None:
        self.account = account
        self.platform = platform.lower()
        self.vertical = vertical
        self.overlap = overlap
        self.scorer = scorer

        if self.platform not in PLATFORM_CONFIG:
            raise ValueError(
                f"Unsupported platform {platform!r}. "
                f"Choose from: {list(PLATFORM_CONFIG)}"
            )

        self._cfg = PLATFORM_CONFIG[self.platform]
        self.segment_duration: float = (
            segment_duration
            if segment_duration is not None
            else float(self._cfg["target_duration"])
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        source_video: str,
        output_dir: str,
        top_n: int = 5,
        clip_duration: Optional[float] = None,
    ) -> ReelResult:
        """
        Extract the top *top_n* reels from *source_video*.

        Args:
            source_video:  Path to the input video file.
            output_dir:    Directory where extracted reels will be saved
                           (created automatically if it does not exist).
            top_n:         Number of reels to extract.
            clip_duration: Override the clip length (seconds).  Defaults to
                           the pipeline's ``segment_duration``.

        Returns:
            A :class:`ReelResult` containing :class:`ReelClip` entries for
            every exported reel plus a JSON manifest written to *output_dir*.
        """
        try:
            from moviepy.editor import VideoFileClip
        except ImportError as exc:
            raise ImportError(
                "moviepy is required.  Install with:  pip install moviepy"
            ) from exc

        import numpy as np  # noqa: F401 — imported for scorer

        source_path = Path(source_video)
        if not source_path.exists():
            raise FileNotFoundError(f"Source video not found: {source_video}")

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        effective_duration = clip_duration if clip_duration is not None else self.segment_duration
        effective_duration = min(effective_duration, self._cfg["max_duration"])

        # ---- load --------------------------------------------------------
        print(f"[ReelPipeline] Loading  : {source_path.name}")
        video = VideoFileClip(str(source_path))
        total_dur = video.duration
        print(
            f"[ReelPipeline] Duration : {total_dur:.1f}s  "
            f"| platform={self.platform}  account={self.account}"
        )

        # ---- analyse -----------------------------------------------------
        candidates = self._build_candidates(total_dur, effective_duration)
        print(f"[ReelPipeline] Scoring  : {len(candidates)} candidate windows …")
        scored = self._score_candidates(video, candidates)

        # ---- select ------------------------------------------------------
        top = self._select_top_n(scored, top_n, effective_duration)
        print(f"[ReelPipeline] Selected : {len(top)} clips")

        # ---- export ------------------------------------------------------
        stem = source_path.stem
        reels: list[ReelClip] = []

        for rank, (t_start, t_end, score) in enumerate(top, start=1):
            filename = (
                f"{self.account}__{self.platform}__reel{rank:02d}__{stem}.mp4"
            )
            out_path = out_dir / filename
            print(f"[ReelPipeline] Exporting: [{rank}/{len(top)}] {filename}")

            clip = video.subclip(t_start, t_end)
            if self.vertical:
                clip = self._crop_vertical(clip)

            clip.write_videofile(
                str(out_path),
                fps=self._cfg["fps"],
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None,
            )
            clip.close()

            reels.append(
                ReelClip(
                    path=str(out_path),
                    start_time=t_start,
                    end_time=t_end,
                    duration=t_end - t_start,
                    score=score,
                    rank=rank,
                )
            )

        video.close()

        result = ReelResult(
            source_video=str(source_path),
            output_dir=str(out_dir),
            account=self.account,
            platform=self.platform,
            reels=reels,
        )
        manifest_path = out_dir / f"{stem}__manifest.json"
        self._write_manifest(result, manifest_path)
        print(f"[ReelPipeline] Manifest : {manifest_path}")
        print(f"[ReelPipeline] Done.")

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_candidates(
        self, total_duration: float, clip_duration: float
    ) -> list[tuple[float, float]]:
        """Return (start, end) pairs using a sliding window."""
        step = clip_duration * (1.0 - self.overlap)
        min_dur = self._cfg["min_duration"]
        candidates: list[tuple[float, float]] = []
        t = 0.0
        while t + min_dur < total_duration:
            end = min(t + clip_duration, total_duration)
            if end - t >= min_dur:
                candidates.append((t, end))
            t += step
        return candidates

    def _score_candidates(
        self,
        video,
        candidates: list[tuple[float, float]],
    ) -> list[tuple[float, float, float]]:
        """Return *(start, end, score)* for every candidate."""
        scored: list[tuple[float, float, float]] = []
        for start, end in candidates:
            clip = video.subclip(start, end)
            score = self._audio_energy(clip)
            scored.append((start, end, score))
            clip.close()
        return scored

    def _audio_energy(self, clip) -> float:
        """Mean RMS audio energy; 0.0 if no audio track."""
        import numpy as np

        if clip.audio is None:
            return 0.0
        try:
            arr = clip.audio.to_soundarray(fps=22_050)
            if arr.ndim > 1:
                arr = arr.mean(axis=1)
            return float(np.sqrt(np.mean(arr ** 2)))
        except Exception:
            return 0.0

    def _select_top_n(
        self,
        scored: list[tuple[float, float, float]],
        top_n: int,
        clip_duration: float,
    ) -> list[tuple[float, float, float]]:
        """
        Greedily pick the top-*top_n* non-overlapping segments (highest score
        first), then return them sorted chronologically.
        """
        by_score = sorted(scored, key=lambda x: x[2], reverse=True)
        selected: list[tuple[float, float, float]] = []

        for start, end, score in by_score:
            if len(selected) >= top_n:
                break
            overlaps = any(
                not (end <= s or start >= e) for s, e, _ in selected
            )
            if not overlaps:
                selected.append((start, end, score))

        return sorted(selected, key=lambda x: x[0])

    def _crop_vertical(self, clip):
        """Center-crop to 9:16.  Returns the clip unchanged if already taller than wide."""
        from moviepy.video.fx.all import crop

        w, h = clip.size
        target_w = int(h * 9 / 16)

        if target_w >= w:
            # Already portrait or square — no crop needed.
            return clip

        x1 = (w - target_w) / 2
        return crop(clip, x1=x1, x2=x1 + target_w)

    def _write_manifest(self, result: ReelResult, path: Path) -> None:
        """Persist run metadata as JSON next to the exported reels."""
        data = {
            "account": result.account,
            "platform": result.platform,
            "vertical": self.vertical,
            "source_video": result.source_video,
            "output_dir": result.output_dir,
            "reels": [
                {
                    "rank": r.rank,
                    "path": r.path,
                    "start_time": r.start_time,
                    "end_time": r.end_time,
                    "duration": r.duration,
                    "score": r.score,
                }
                for r in result.reels
            ],
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
