"""
DaVinci Resolve API utilities for Flamenco 11-cam pipeline.
Shared functions used by all pipeline scripts.
"""

import json
import os
import sys
import time
import logging
from pathlib import Path

logger = logging.getLogger("flamenco_pipeline")

# Config paths
CONFIG_DIR = Path(__file__).parent.parent / "config"
CAMERA_PROFILES_PATH = CONFIG_DIR / "camera_profiles.json"
FLAMENCO_CONFIG_PATH = CONFIG_DIR / "flamenco_config.json"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2.0


def _load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_camera_profiles() -> dict:
    """Load camera_profiles.json and return the cameras dict."""
    data = _load_json(CAMERA_PROFILES_PATH)
    return data["cameras"]


def get_flamenco_config() -> dict:
    """Load flamenco_config.json."""
    return _load_json(FLAMENCO_CONFIG_PATH)


def get_camera_profile(camera_key: str) -> dict:
    """Get a single camera profile by key."""
    profiles = get_camera_profiles()
    if camera_key not in profiles:
        raise KeyError(f"Camera profile not found: {camera_key}")
    return profiles[camera_key]


# ---------------------------------------------------------------------------
# DaVinci Resolve API wrappers
# ---------------------------------------------------------------------------

def get_resolve():
    """Connect to DaVinci Resolve scripting API."""
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        # Fallback: try the environment-based path
        resolve_script_api = os.environ.get(
            "RESOLVE_SCRIPT_API",
            "/opt/resolve/Developer/Scripting/Modules",
        )
        if resolve_script_api not in sys.path:
            sys.path.append(resolve_script_api)
        import DaVinciResolveScript as dvr

    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        raise ConnectionError(
            "Could not connect to DaVinci Resolve. "
            "Ensure Resolve is running with scripting enabled."
        )
    return resolve


def get_project_manager():
    """Get the ProjectManager from Resolve."""
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    if pm is None:
        raise RuntimeError("Failed to get ProjectManager")
    return pm


def get_current_project():
    """Get the currently open project."""
    pm = get_project_manager()
    project = pm.GetCurrentProject()
    if project is None:
        raise RuntimeError("No project is currently open")
    return project


def get_media_pool():
    """Get the MediaPool from the current project."""
    project = get_current_project()
    pool = project.GetMediaPool()
    if pool is None:
        raise RuntimeError("Failed to get MediaPool")
    return pool


def retry(func, *args, max_retries=MAX_RETRIES, delay=RETRY_DELAY, **kwargs):
    """Retry a function call with exponential backoff."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(
                "Attempt %d/%d failed: %s. Retrying in %.1fs...",
                attempt + 1, max_retries, e, delay,
            )
            time.sleep(delay)
            delay *= 2
    raise last_error


# ---------------------------------------------------------------------------
# Media Pool helpers
# ---------------------------------------------------------------------------

def create_media_pool_folder(pool, path: str):
    """
    Create a nested folder structure in the MediaPool.
    path: slash-separated path like 'Master/_Source/CAM01_SIGMAfp'
    Returns the deepest Folder object.
    """
    parts = path.strip("/").split("/")
    root = pool.GetRootFolder()
    current = root

    for part in parts:
        # Check if subfolder already exists
        existing = None
        for sub in current.GetSubFolderList():
            if sub.GetName() == part:
                existing = sub
                break
        if existing:
            current = existing
        else:
            new_folder = pool.AddSubFolder(current, part)
            if new_folder is None:
                raise RuntimeError(f"Failed to create folder: {part} under {current.GetName()}")
            current = new_folder

    return current


# ---------------------------------------------------------------------------
# Camera detection
# ---------------------------------------------------------------------------

def detect_camera(clip) -> str:
    """
    Detect camera type from a MediaPool clip using camera_profiles.json rules.
    Returns the camera key (e.g. 'nikon_zr') or 'unknown'.
    """
    profiles = get_camera_profiles()

    clip_name = clip.GetName() or ""
    clip_props = clip.GetClipProperty() if hasattr(clip, "GetClipProperty") else {}
    codec = clip_props.get("Video Codec", "") if isinstance(clip_props, dict) else ""
    resolution = clip_props.get("Resolution", "") if isinstance(clip_props, dict) else ""

    # Get metadata
    metadata = clip.GetMetadata() if hasattr(clip, "GetMetadata") else {}
    exif_make = metadata.get("Camera Manufacturer", "") if isinstance(metadata, dict) else ""
    exif_model = metadata.get("Camera Model", "") if isinstance(metadata, dict) else ""

    # File extension
    file_path = clip_props.get("File Path", "") if isinstance(clip_props, dict) else ""
    file_ext = Path(file_path).suffix.lower() if file_path else ""

    best_match = None
    best_score = 0

    for cam_key, profile in profiles.items():
        detection = profile.get("detection", {})
        score = 0

        # Filename pattern matching
        for pattern in detection.get("filename_patterns", []):
            if pattern.upper() in clip_name.upper():
                score += 1

        # Codec matching
        for c in detection.get("codecs", []):
            if c.lower() in codec.lower():
                score += 2

        # EXIF matching (strong signal)
        if detection.get("exif_make") and detection["exif_make"].lower() in exif_make.lower():
            score += 3
        if detection.get("exif_model") and detection["exif_model"].lower() in exif_model.lower():
            score += 4

        # File extension matching (critical for Nikon ZR vs Z6III)
        for ext in detection.get("file_extensions", []):
            if file_ext == ext:
                score += 5

        # Resolution hint (critical for URSA Mini vs BM Production Camera)
        res_hint = detection.get("resolution_hint", "")
        if res_hint and res_hint in resolution:
            score += 3

        if score > best_score:
            best_score = score
            best_match = cam_key

    if best_match and best_score >= 3:
        return best_match

    logger.warning("Could not detect camera for clip: %s (best score: %d)", clip_name, best_score)
    return "unknown"


# ---------------------------------------------------------------------------
# PowerGrade / Node helpers
# ---------------------------------------------------------------------------

def apply_powergrade(clip, drx_path: str) -> bool:
    """
    Apply a PowerGrade (.drx) file to a clip.
    Returns True on success.
    """
    drx = Path(drx_path).expanduser()
    if not drx.exists():
        raise FileNotFoundError(f"PowerGrade file not found: {drx}")

    success = clip.ApplyGrade(str(drx))
    if not success:
        logger.error("Failed to apply PowerGrade %s to clip %s", drx.name, clip.GetName())
    return bool(success)


def set_cst_input(node, color_space: str, gamma: str) -> bool:
    """
    Set the Color Space Transform input parameters on a corrector node.
    """
    try:
        node.SetParam("colorSpaceInputColorSpace", color_space)
        node.SetParam("colorSpaceInputGamma", gamma)
        return True
    except Exception as e:
        logger.error("Failed to set CST input on node: %s", e)
        return False


def set_cst_output(node, color_space: str = "Rec.709", gamma: str = "Gamma 2.4") -> bool:
    """
    Set the Color Space Transform output parameters on a corrector node.
    """
    try:
        node.SetParam("colorSpaceOutputColorSpace", color_space)
        node.SetParam("colorSpaceOutputGamma", gamma)
        return True
    except Exception as e:
        logger.error("Failed to set CST output on node: %s", e)
        return False


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging(script_name: str) -> logging.Logger:
    """Configure logging for a pipeline script."""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"flamenco_{script_name}_{timestamp}.log"

    handler_file = logging.FileHandler(log_file, encoding="utf-8")
    handler_console = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler_file.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    root_logger = logging.getLogger("flamenco_pipeline")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler_file)
    root_logger.addHandler(handler_console)

    root_logger.info("=== %s started ===", script_name)
    root_logger.info("Log file: %s", log_file)

    return root_logger
