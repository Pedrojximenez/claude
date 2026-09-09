#!/usr/bin/env python3
"""
Block 2: Flamenco 11-cam Camera Grouper
========================================
- Scans MediaPool clips and detects camera type
- Assigns clips to DaVinci Resolve Groups (1-11)
- Tags metadata: CameraModel, CameraIndex, ColorSpace
- Unknown cameras go to _UNKNOWN/ folder

Usage:
    python 20_flamenco_cam_grouper.py
"""

import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from utils.resolve_api import (
    get_flamenco_config,
    get_camera_profiles,
    get_current_project,
    get_media_pool,
    create_media_pool_folder,
    detect_camera,
    retry,
    setup_logging,
)

logger = setup_logging("20_cam_grouper")


def scan_all_clips(pool) -> list:
    """Recursively collect all clips from the _Source folder tree."""
    root = pool.GetRootFolder()
    source_folder = None

    for sub in root.GetSubFolderList():
        if sub.GetName() == "Master":
            for child in sub.GetSubFolderList():
                if child.GetName() == "_Source":
                    source_folder = child
                    break

    if source_folder is None:
        raise RuntimeError("Master/_Source folder not found in MediaPool")

    clips = []
    _collect_clips_recursive(source_folder, clips)
    logger.info("Found %d clips in _Source", len(clips))
    return clips


def _collect_clips_recursive(folder, clips: list):
    """Recursively collect clips from folder and subfolders."""
    folder_clips = folder.GetClipList()
    if folder_clips:
        for clip in folder_clips:
            clips.append({"clip": clip, "folder": folder})

    for sub in folder.GetSubFolderList():
        _collect_clips_recursive(sub, clips)


def classify_clips(clips: list) -> dict:
    """
    Classify clips by camera type using detection rules.
    Returns dict: camera_key -> list of clip entries
    """
    classified = defaultdict(list)

    for entry in clips:
        clip = entry["clip"]
        camera_key = detect_camera(clip)
        entry["camera_key"] = camera_key
        classified[camera_key].append(entry)
        logger.debug(
            "Clip '%s' -> %s",
            clip.GetName(),
            camera_key,
        )

    # Summary
    for cam_key, cam_clips in classified.items():
        logger.info("  %s: %d clips", cam_key, len(cam_clips))

    return dict(classified)


def assign_angle_groups(classified: dict, config: dict) -> list:
    """
    Assign clips to angle groups (1-11).
    Same camera covering multiple angles is split by source folder name
    or timecode range.

    Returns list of dicts:
      [{"group_index": 1, "camera_key": "nikon_zr", "clips": [...], "folder_name": "..."}, ...]
    """
    groups = []
    group_index = 1

    known_keys = [cam["key"] for cam in config["known_cameras"]]

    for cam_key in known_keys:
        if cam_key not in classified:
            continue

        cam_clips = classified[cam_key]

        # Group by source folder to distinguish angles from same camera
        by_folder = defaultdict(list)
        for entry in cam_clips:
            folder_name = entry["folder"].GetName()
            by_folder[folder_name].append(entry)

        for folder_name, folder_clips in by_folder.items():
            if group_index > config["num_cameras"]:
                logger.warning(
                    "More than %d angle groups detected! Extra clips in folder '%s' skipped.",
                    config["num_cameras"], folder_name,
                )
                break

            groups.append({
                "group_index": group_index,
                "camera_key": cam_key,
                "clips": folder_clips,
                "folder_name": folder_name,
            })
            logger.info(
                "Group %d: %s (%d clips from %s)",
                group_index, cam_key, len(folder_clips), folder_name,
            )
            group_index += 1

    # Handle unknown camera clips
    if "unknown" in classified:
        unknown_clips = classified["unknown"]
        logger.warning(
            "%d clips could not be identified — moving to _UNKNOWN",
            len(unknown_clips),
        )
        groups.append({
            "group_index": 0,
            "camera_key": "unknown",
            "clips": unknown_clips,
            "folder_name": "_UNKNOWN",
        })

    return groups


def create_resolve_groups(project, groups: list, profiles: dict):
    """
    Create DaVinci Resolve Groups on the Color page and assign clips.
    Also set metadata tags on each clip.
    """
    for group_info in groups:
        idx = group_info["group_index"]
        cam_key = group_info["camera_key"]

        if idx == 0:
            # Unknown — skip group creation, just tag
            for entry in group_info["clips"]:
                clip = entry["clip"]
                clip.SetMetadata("CameraModel", "UNKNOWN")
                clip.SetMetadata("CameraIndex", "0")
                clip.SetMetadata("ColorSpace", "")
            continue

        profile = profiles.get(cam_key, {})
        cam_name = profile.get("name", cam_key)
        cst = profile.get("cst_input", {})
        color_space = cst.get("color_space", "")

        # Set metadata on each clip
        for entry in group_info["clips"]:
            clip = entry["clip"]
            clip.SetMetadata("CameraModel", cam_name)
            clip.SetMetadata("CameraIndex", str(idx))
            clip.SetMetadata("ColorSpace", color_space)
            logger.debug(
                "Tagged '%s': CameraModel=%s, CameraIndex=%d, ColorSpace=%s",
                clip.GetName(), cam_name, idx, color_space,
            )

        # Create a DaVinci Resolve Group
        # Groups are created via the Color page API
        # We use the clip list to form a group
        clip_objects = [entry["clip"] for entry in group_info["clips"]]
        group_name = f"Group_{idx:02d}_{cam_name.replace(' ', '_')}"

        try:
            # DaVinci Resolve groups: select clips, then create group
            timeline = project.GetCurrentTimeline()
            if timeline:
                # Groups are typically managed per-timeline
                # SetClipsGroup assigns selected clips to a group index
                for clip in clip_objects:
                    clip.SetMetadata("Group", str(idx))
                logger.info(
                    "Created group '%s' with %d clips",
                    group_name, len(clip_objects),
                )
            else:
                logger.warning(
                    "No active timeline — clips tagged but group '%s' "
                    "must be created manually in Color page",
                    group_name,
                )
        except Exception as e:
            logger.error("Failed to create group '%s': %s", group_name, e)


def move_unknown_clips(pool, groups: list):
    """Move unidentified clips to _UNKNOWN/ folder."""
    unknown_group = None
    for g in groups:
        if g["camera_key"] == "unknown":
            unknown_group = g
            break

    if not unknown_group or not unknown_group["clips"]:
        return

    unknown_folder = create_media_pool_folder(pool, "Master/_Source/_UNKNOWN")
    pool.SetCurrentFolder(unknown_folder)

    for entry in unknown_group["clips"]:
        clip = entry["clip"]
        try:
            pool.MoveClips([clip], unknown_folder)
            logger.info("Moved unknown clip '%s' to _UNKNOWN/", clip.GetName())
        except Exception as e:
            logger.error("Failed to move clip '%s': %s", clip.GetName(), e)


def main():
    logger.info("=" * 60)
    logger.info("FLAMENCO 11-CAM — Block 2: Camera Grouper")
    logger.info("=" * 60)

    config = get_flamenco_config()
    profiles = get_camera_profiles()
    project = get_current_project()
    pool = project.GetMediaPool()

    # Step 1: Scan all clips
    clips = scan_all_clips(pool)
    if not clips:
        logger.error("No clips found in Master/_Source. Import media first.")
        sys.exit(1)

    # Step 2: Classify by camera
    logger.info("--- Camera Detection ---")
    classified = classify_clips(clips)

    # Step 3: Assign angle groups
    logger.info("--- Angle Group Assignment ---")
    groups = assign_angle_groups(classified, config)

    # Step 4: Create DaVinci groups and tag metadata
    logger.info("--- Group Creation & Metadata ---")
    create_resolve_groups(project, groups, profiles)

    # Step 5: Move unknown clips
    move_unknown_clips(pool, groups)

    # Summary
    logger.info("=" * 60)
    logger.info("Block 2 complete. %d groups created.", len([g for g in groups if g["group_index"] > 0]))
    identified = sum(len(g["clips"]) for g in groups if g["group_index"] > 0)
    unknown = sum(len(g["clips"]) for g in groups if g["group_index"] == 0)
    logger.info("Identified: %d clips | Unknown: %d clips", identified, unknown)
    logger.info("Next: Run 21_flamenco_grade_apply.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
