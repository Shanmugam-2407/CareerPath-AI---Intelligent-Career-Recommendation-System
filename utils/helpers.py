"""
Helper functions for local JSON storage and safe I/O.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


def ensure_parent_dir(file_path: Union[str, Path]) -> None:
    """Ensure the parent directory for a given file path exists."""
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)


def save_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> bool:
    """
    Safely save Python data structure to a JSON file.
    Creates parent directories if they don't exist.
    """
    try:
        p = Path(file_path)
        ensure_parent_dir(p)
        temp_file = p.with_suffix(p.suffix + ".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, default=str)
        # Atomic replace
        if os.path.exists(p):
            os.replace(temp_file, p)
        else:
            temp_file.rename(p)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False


def load_json(file_path: Union[str, Path], default: Optional[Any] = None) -> Any:
    """
    Safely load JSON file with error handling for missing, empty, or corrupted files.
    Returns `default` if the file doesn't exist, is empty, or has invalid JSON.
    """
    if default is None:
        default = {}
    p = Path(file_path)
    if not p.exists() or p.stat().st_size == 0:
        return default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Error loading JSON from {file_path}: {e}. Returning default.")
        return default


def update_json(file_path: Union[str, Path], new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing JSON object file with dictionary new_data.
    """
    current_data = load_json(file_path, default={})
    if not isinstance(current_data, dict):
        current_data = {}
    current_data.update(new_data)
    save_json(file_path, current_data)
    return current_data

