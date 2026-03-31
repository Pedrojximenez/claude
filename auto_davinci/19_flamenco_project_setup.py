#!/usr/bin/env python3
"""
Block 1: Flamenco 11-cam Project Setup
=======================================
- Creates DaVinci Resolve project with correct timeline settings
- Builds MediaPool folder structure for 11 cameras
- Imports PowerGrade .drx files from ~/Desktop/

Usage:
    python 19_flamenco_project_setup.py
"""

import sys
import time
from pathlib import Path

# Add parent to path for utils import
sys.path.insert(0, str(Path(__file__).parent))

from utils.resolve_api import (
    get_flamenco_config,
    get_camera_profiles,
    get_resolve,
    get_project_manager,
    create_media_pool_folder,
    retry,
    setup_logging,
)

logger = setup_logging("19_project_setup")


def create_project(config: dict):
    """Create a new DaVinci Resolve project with Flamenco settings."""
    resolve = get_resolve()
    pm = resolve.GetProjectManager()

    # Generate project name with date
    date_str = time.strftime("%Y%m%d")
    project_name = config["project_name"].replace("{date}", date_str)

    logger.info("Creating project: %s", project_name)

    # Check if project already exists
    existing = pm.LoadProject(project_name)
    if existing:
        logger.warning("Project '%s' already exists. Using existing project.", project_name)
        return existing

    project = pm.CreateProject(project_name)
    if project is None:
        raise RuntimeError(f"Failed to create project: {project_name}")

    logger.info("Project created: %s", project_name)
    return project


def configure_timeline_settings(project, config: dict):
    """Set timeline resolution, frame rate, color science, and gamma."""
    timeline_cfg = config["timeline"]

    width, height = timeline_cfg["resolution"].split("x")

    settings = {
        "timelineFrameRate": str(timeline_cfg["frame_rate"]),
        "timelineResolutionWidth": width,
        "timelineResolutionHeight": height,
        "colorScienceMode": "davinciYRGBColorManagedv2",
        "rcmTimelineColorSpace": timeline_cfg["color_science"],
        "rcmTimelineGamma": timeline_cfg["gamma"],
        "separateColorSpaceAndGamma": "1",
    }

    for key, value in settings.items():
        result = project.SetSetting(key, value)
        if result:
            logger.info("Set %s = %s", key, value)
        else:
            logger.warning("Failed to set %s = %s (may require project reload)", key, value)

    logger.info(
        "Timeline: %sx%s @ %sfps | %s / %s",
        width, height,
        timeline_cfg["frame_rate"],
        timeline_cfg["color_science"],
        timeline_cfg["gamma"],
    )


def build_media_pool_structure(project, config: dict):
    """
    Build the MediaPool folder structure:
    Master/
    ├── _Source/
    │   ├── CAM01_.../
    │   ...
    │   └── CAM11_.../
    ├── _Audio/
    ├── _PowerGrade/
    └── _Proxy/
    """
    pool = project.GetMediaPool()

    # Top-level folders
    for folder in ["_Source", "_Audio", "_PowerGrade", "_Proxy"]:
        create_media_pool_folder(pool, f"Master/{folder}")
        logger.info("Created folder: Master/%s", folder)

    # Camera source folders (11 angles)
    # First, assign camera names to the 11 slots
    # We use config's known_cameras; some cameras cover multiple angles
    cam_labels = _generate_camera_labels(config)

    for i, label in enumerate(cam_labels, 1):
        folder_name = f"CAM{i:02d}_{label}"
        create_media_pool_folder(pool, f"Master/_Source/{folder_name}")
        logger.info("Created folder: Master/_Source/%s", folder_name)

    # Create _UNKNOWN folder for undetected clips
    create_media_pool_folder(pool, "Master/_Source/_UNKNOWN")
    logger.info("Created folder: Master/_Source/_UNKNOWN")

    return pool


def _generate_camera_labels(config: dict) -> list[str]:
    """
    Generate 11 camera slot labels.
    5 cameras x 11 angles — exact assignment will be determined
    at grouper stage, but we pre-create folders for all 11.
    """
    cameras = config["known_cameras"]
    labels = []

    # Distribution: create slots based on known cameras
    # SIGMA fp is not in this shoot's known_cameras, but we prepare
    # generic slots that will be renamed by the grouper
    for cam in cameras:
        labels.append(cam["name"].replace(" ", ""))

    # Fill remaining slots up to 11
    remaining = config["num_cameras"] - len(labels)
    for i in range(remaining):
        # Extra angle slots — will be assigned at grouping time
        labels.append(f"ANGLE{len(labels) + 1:02d}")

    return labels[:config["num_cameras"]]


def import_powergrade_files(pool, config: dict):
    """Import PowerGrade .drx files from ~/Desktop/ into _PowerGrade folder."""
    pg_source = Path(config["powergrade_source"]).expanduser()
    pg_folder = None

    # Navigate to _PowerGrade folder
    root = pool.GetRootFolder()
    for sub in root.GetSubFolderList():
        if sub.GetName() == "Master":
            for child in sub.GetSubFolderList():
                if child.GetName() == "_PowerGrade":
                    pg_folder = child
                    break

    if pg_folder is None:
        raise RuntimeError("_PowerGrade folder not found in MediaPool")

    pool.SetCurrentFolder(pg_folder)

    imported_count = 0
    for look_key, filename in config["powergrade_files"].items():
        drx_path = pg_source / filename
        if drx_path.exists():
            result = pool.ImportMedia([str(drx_path)])
            if result:
                logger.info("Imported PowerGrade: %s (%s)", filename, look_key)
                imported_count += 1
            else:
                logger.error("Failed to import PowerGrade: %s", filename)
        else:
            logger.warning(
                "PowerGrade file not found: %s — "
                "Place .drx files in %s before running grade_apply.",
                drx_path, pg_source,
            )

    logger.info("Imported %d/%d PowerGrade files", imported_count, len(config["powergrade_files"]))
    return imported_count


def main():
    logger.info("=" * 60)
    logger.info("FLAMENCO 11-CAM — Block 1: Project Setup")
    logger.info("=" * 60)

    config = get_flamenco_config()

    # Step 1: Create project
    project = retry(create_project, config)

    # Step 2: Configure timeline settings
    configure_timeline_settings(project, config)

    # Step 3: Build MediaPool folder structure
    pool = build_media_pool_structure(project, config)

    # Step 4: Import PowerGrade files
    import_powergrade_files(pool, config)

    logger.info("=" * 60)
    logger.info("Block 1 complete. Project is ready for media import.")
    logger.info(
        "Next: Import media into CAM01-CAM11 folders, "
        "then run 20_flamenco_cam_grouper.py"
    )
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
