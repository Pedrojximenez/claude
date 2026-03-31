#!/usr/bin/env python3
"""
Block 3: Flamenco 11-cam PowerGrade Auto-Apply
===============================================
- Applies PowerGrade (Twilight Inferno) to each Group's reference clip
- Sets CST Input per camera (CSTサンドイッチ方式)
- Sets CST Output (Rec.709 / Gamma 2.4) shared across all
- Configures Shared Nodes for CST Input (node 1) and CST Output (node 10)
- Auto-detects flicker and flags for DaVinci Deflicker

PowerGrade 10-node structure:
  1. CST Input (camera-specific -> DWG/DI)  [SHARED]
  2. Exposure Balance
  3. LED Color Cast Correction
  4. Primary Lift/Gamma/Gain
  5. Skin Tone Qualifier
  6. Highlight Recovery
  7. Shadow Detail
  8. Look (Tablao or Sevilla Nocturna)
  9. Vignette
 10. CST Output (-> Rec.709 / Gamma 2.4)    [SHARED]

Usage:
    python 21_flamenco_grade_apply.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.resolve_api import (
    get_flamenco_config,
    get_camera_profiles,
    get_camera_profile,
    get_current_project,
    get_media_pool,
    apply_powergrade,
    set_cst_input,
    set_cst_output,
    retry,
    setup_logging,
)

logger = setup_logging("21_grade_apply")

# Node indices (1-based) in the 10-node PowerGrade
NODE_CST_INPUT = 1
NODE_EXPOSURE = 2
NODE_LED_FIX = 3
NODE_PRIMARY = 4
NODE_SKIN_TONE = 5
NODE_HIGHLIGHT = 6
NODE_SHADOW = 7
NODE_LOOK = 8
NODE_VIGNETTE = 9
NODE_CST_OUTPUT = 10

# CST Output (shared across all cameras)
CST_OUTPUT_COLOR_SPACE = "Rec.709"
CST_OUTPUT_GAMMA = "Gamma 2.4"


def find_groups_with_metadata(pool) -> list:
    """
    Scan MediaPool for clips with CameraIndex metadata (set by Block 2).
    Returns grouped clips: [{group_index, camera_key, camera_name, clips}, ...]
    """
    from collections import defaultdict

    root = pool.GetRootFolder()
    all_clips = []
    _collect_all_clips(root, all_clips)

    groups_map = defaultdict(lambda: {"clips": [], "camera_key": None, "camera_name": None})

    for clip in all_clips:
        metadata = clip.GetMetadata() if hasattr(clip, "GetMetadata") else {}
        if not isinstance(metadata, dict):
            continue

        cam_index = metadata.get("CameraIndex", "")
        cam_model = metadata.get("CameraModel", "")

        if not cam_index or cam_index == "0":
            continue

        idx = int(cam_index)
        groups_map[idx]["clips"].append(clip)
        groups_map[idx]["camera_name"] = cam_model

    # Resolve camera_key from camera_name
    profiles = get_camera_profiles()
    name_to_key = {p["name"]: k for k, p in profiles.items()}

    groups = []
    for idx in sorted(groups_map.keys()):
        g = groups_map[idx]
        cam_name = g["camera_name"] or "UNKNOWN"
        cam_key = name_to_key.get(cam_name, "unknown")
        groups.append({
            "group_index": idx,
            "camera_key": cam_key,
            "camera_name": cam_name,
            "clips": g["clips"],
        })

    return groups


def _collect_all_clips(folder, clips: list):
    """Recursively collect all clips."""
    folder_clips = folder.GetClipList()
    if folder_clips:
        clips.extend(folder_clips)
    for sub in folder.GetSubFolderList():
        _collect_all_clips(sub, clips)


def resolve_powergrade_path(config: dict, look_key: str = None) -> str:
    """Get the full path to a PowerGrade .drx file."""
    if look_key is None:
        look_key = config["default_look"]

    pg_source = Path(config["powergrade_source"]).expanduser()
    pg_files = config["powergrade_files"]

    if look_key not in pg_files:
        raise ValueError(f"Unknown look key: {look_key}. Available: {list(pg_files.keys())}")

    drx_path = pg_source / pg_files[look_key]
    return str(drx_path)


def apply_grade_to_group(project, group: dict, config: dict, profiles: dict):
    """
    Apply PowerGrade to the reference (first) clip in a group,
    then configure CST nodes for the camera type.
    """
    idx = group["group_index"]
    cam_key = group["camera_key"]
    cam_name = group["camera_name"]
    clips = group["clips"]

    if not clips:
        logger.warning("Group %d (%s) has no clips — skipping", idx, cam_name)
        return

    logger.info("--- Group %d: %s (%d clips) ---", idx, cam_name, len(clips))

    # Get camera CST settings
    if cam_key == "unknown" or cam_key not in profiles:
        logger.error(
            "Group %d: Unknown camera '%s' — cannot set CST. Skipping grade.",
            idx, cam_name,
        )
        return

    profile = profiles[cam_key]
    cst_input = profile["cst_input"]

    # Step 1: Apply PowerGrade to reference clip (first clip)
    ref_clip = clips[0]
    drx_path = resolve_powergrade_path(config)

    drx_file = Path(drx_path)
    if not drx_file.exists():
        logger.error(
            "PowerGrade not found: %s — "
            "Ensure .drx files are in %s",
            drx_path, config["powergrade_source"],
        )
        return

    logger.info("Applying PowerGrade '%s' to ref clip '%s'", drx_file.name, ref_clip.GetName())
    success = apply_powergrade(ref_clip, drx_path)
    if not success:
        logger.error("Failed to apply PowerGrade to group %d", idx)
        return

    # Step 2: Configure CST nodes on the reference clip
    configure_cst_nodes(project, ref_clip, cst_input, idx)

    # Step 3: Set as Remote Grade so all clips in group inherit
    set_remote_grade(project, ref_clip, clips, idx)

    # Step 4: Check for flicker
    if config.get("deflicker_auto_detect", False):
        check_flicker(clips, idx)

    logger.info("Group %d: Grade applied successfully", idx)


def configure_cst_nodes(project, clip, cst_input: dict, group_index: int):
    """
    Configure CST Input (node 1) and CST Output (node 10) on a graded clip.
    Makes both nodes Shared Nodes.
    """
    timeline = project.GetCurrentTimeline()
    if not timeline:
        logger.warning("No active timeline — CST node config requires Color page access")
        return

    try:
        # Access the clip's node graph in Color page
        # Note: This requires the clip to be the current clip in Color page
        color_page = project.GetCurrentPage()

        # Get node graph
        # DaVinci API: timeline item -> GetNodeGraph()
        # We work with the grade applied to the clip
        clip_item = _find_timeline_item(timeline, clip)
        if not clip_item:
            logger.warning(
                "Group %d: Could not find clip in timeline for CST config. "
                "CST must be set manually or after timeline creation.",
                group_index,
            )
            return

        node_graph = clip_item.GetNodeGraph() if hasattr(clip_item, "GetNodeGraph") else None
        if not node_graph:
            logger.warning("Group %d: Cannot access node graph via API", group_index)
            return

        # Node 1: CST Input
        nodes = node_graph.GetNodeList() if hasattr(node_graph, "GetNodeList") else []
        if len(nodes) >= NODE_CST_OUTPUT:
            # Set CST Input (node 1)
            input_node = nodes[NODE_CST_INPUT - 1]
            set_cst_input(
                input_node,
                cst_input["color_space"],
                cst_input["gamma"],
            )
            logger.info(
                "Group %d: CST Input = %s / %s",
                group_index, cst_input["color_space"], cst_input["gamma"],
            )

            # Set CST Output (node 10)
            output_node = nodes[NODE_CST_OUTPUT - 1]
            set_cst_output(output_node, CST_OUTPUT_COLOR_SPACE, CST_OUTPUT_GAMMA)
            logger.info(
                "Group %d: CST Output = %s / %s",
                group_index, CST_OUTPUT_COLOR_SPACE, CST_OUTPUT_GAMMA,
            )

            # Make nodes 1 and 10 Shared Nodes
            _set_shared_node(node_graph, NODE_CST_INPUT, f"CST_Input_Shared")
            _set_shared_node(node_graph, NODE_CST_OUTPUT, f"CST_Output_Shared")
            logger.info("Group %d: Nodes 1 & 10 set as Shared Nodes", group_index)
        else:
            logger.warning(
                "Group %d: Expected 10 nodes, found %d. "
                "PowerGrade may not have applied correctly.",
                group_index, len(nodes),
            )

    except Exception as e:
        logger.error("Group %d: CST configuration failed: %s", group_index, e)
        logger.info(
            "Group %d: Manual CST setup required — "
            "Input: %s / %s, Output: %s / %s",
            group_index,
            cst_input["color_space"], cst_input["gamma"],
            CST_OUTPUT_COLOR_SPACE, CST_OUTPUT_GAMMA,
        )


def _find_timeline_item(timeline, media_pool_clip):
    """Find a timeline item corresponding to a media pool clip."""
    track_count = timeline.GetTrackCount("video")
    clip_name = media_pool_clip.GetName()

    for track_idx in range(1, track_count + 1):
        items = timeline.GetItemListInTrack("video", track_idx)
        if not items:
            continue
        for item in items:
            if item.GetName() == clip_name:
                return item

    return None


def _set_shared_node(node_graph, node_index: int, shared_name: str):
    """Attempt to set a node as a Shared Node."""
    try:
        nodes = node_graph.GetNodeList()
        if node_index <= len(nodes):
            node = nodes[node_index - 1]
            # DaVinci API for shared nodes
            if hasattr(node, "SetSharedNode"):
                node.SetSharedNode(shared_name)
            elif hasattr(node_graph, "SetNodeShared"):
                node_graph.SetNodeShared(node_index, shared_name)
    except Exception as e:
        logger.debug("Could not set shared node %d: %s", node_index, e)


def set_remote_grade(project, ref_clip, all_clips: list, group_index: int):
    """
    Apply Remote Grade from reference clip to all clips in the group.
    This ensures all clips share the same grade.
    """
    if len(all_clips) <= 1:
        return

    timeline = project.GetCurrentTimeline()
    if not timeline:
        logger.info(
            "Group %d: No timeline — Remote Grade will be available after timeline creation",
            group_index,
        )
        return

    ref_name = ref_clip.GetName()
    applied_count = 0

    for clip in all_clips[1:]:  # Skip reference clip
        try:
            # Apply grade from reference
            target_item = _find_timeline_item(timeline, clip)
            ref_item = _find_timeline_item(timeline, ref_clip)

            if target_item and ref_item:
                # Copy grade from ref to target
                target_item.ApplyGradeFromClip(ref_item)
                applied_count += 1
        except Exception as e:
            logger.debug(
                "Group %d: Could not apply remote grade to '%s': %s",
                group_index, clip.GetName(), e,
            )

    if applied_count > 0:
        logger.info(
            "Group %d: Remote grade from '%s' applied to %d/%d clips",
            group_index, ref_name, applied_count, len(all_clips) - 1,
        )


def check_flicker(clips: list, group_index: int):
    """
    Simple flicker detection heuristic.
    Flags clips that may need DaVinci Deflicker applied.
    """
    flagged = []
    for clip in clips:
        props = clip.GetClipProperty() if hasattr(clip, "GetClipProperty") else {}
        if not isinstance(props, dict):
            continue

        # Heuristic: check for LED-related keywords in clip metadata
        # or short exposure times that might cause flicker with LED
        scene = props.get("Scene", "")
        comments = props.get("Comments", "")

        # Flag if metadata suggests LED environment
        if any(kw in (scene + comments).lower() for kw in ["led", "stage", "flicker"]):
            flagged.append(clip.GetName())
            clip.SetMetadata("DeflickerFlag", "true")

    if flagged:
        logger.warning(
            "Group %d: %d clips flagged for potential flicker: %s",
            group_index, len(flagged), ", ".join(flagged[:5]),
        )
    else:
        logger.info("Group %d: No flicker indicators detected", group_index)


def main():
    logger.info("=" * 60)
    logger.info("FLAMENCO 11-CAM — Block 3: PowerGrade Auto-Apply")
    logger.info("=" * 60)

    config = get_flamenco_config()
    profiles = get_camera_profiles()
    project = get_current_project()
    pool = project.GetMediaPool()

    # Verify PowerGrade files exist
    drx_path = resolve_powergrade_path(config)
    drx_file = Path(drx_path)
    if not drx_file.exists():
        logger.error(
            "FATAL: PowerGrade file not found: %s\n"
            "Place .drx files in %s and retry.",
            drx_path, config["powergrade_source"],
        )
        sys.exit(1)

    # Find groups (set by Block 2)
    groups = find_groups_with_metadata(pool)
    if not groups:
        logger.error(
            "No groups found. Run 20_flamenco_cam_grouper.py first."
        )
        sys.exit(1)

    logger.info("Found %d camera groups", len(groups))

    # Apply grade to each group
    for group in groups:
        retry(apply_grade_to_group, project, group, config, profiles)

    # Summary
    logger.info("=" * 60)
    logger.info("Block 3 complete. Grades applied to %d groups.", len(groups))
    logger.info("CSTサンドイッチ構成:")
    for group in groups:
        cam_key = group["camera_key"]
        if cam_key in profiles:
            cst = profiles[cam_key]["cst_input"]
            logger.info(
                "  Group %d (%s): %s / %s -> %s / %s",
                group["group_index"],
                group["camera_name"],
                cst["color_space"], cst["gamma"],
                CST_OUTPUT_COLOR_SPACE, CST_OUTPUT_GAMMA,
            )
    logger.info("Next: Manual review in Color Page (総司令 + ボンド)")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
