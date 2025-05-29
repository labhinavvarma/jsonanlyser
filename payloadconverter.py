import json
import os
from typing import Any, Dict
from uuid import uuid4
from pathlib import Path

def flatten_payload_to_data(payload: Dict[str, Any]) -> Any:
    """
    Extracts the core 'data' from a complex payload structure.
    Assumes the JSON you want is inside a top-level key named 'data'.

    Args:
        payload: A complex or nested dictionary payload.

    Returns:
        The cleaned/extracted data (list or dict).
    """
    if "data" in payload:
        return payload["data"]
    
    # Fallback: try to guess where the main data is
    for key, value in payload.items():
        if isinstance(value, (list, dict)):
            return value

    raise ValueError("No JSON-compatible data structure found in payload.")

def save_json(data: Any, output_dir: str = ".", prefix: str = "converted") -> str:
    """
    Saves a Python dict/list as a JSON file.

    Args:
        data: The Python data (list, dict, etc.)
        output_dir: Folder to save the file in.
        prefix: Prefix for the filename.

    Returns:
        Path to the saved JSON file.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{uuid4().hex[:8]}.json"
    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path

def convert_payload_to_json(payload: Dict[str, Any], output_dir: str = ".") -> str:
    """
    Extracts and saves core JSON content from a complex payload.

    Args:
        payload: Incoming dictionary or nested payload.
        output_dir: Where to save the output JSON file.

    Returns:
        File path to the saved JSON.
    """
    try:
        data = flatten_payload_to_data(payload)
        return save_json(data, output_dir)
    except Exception as e:
        raise RuntimeError(f"Failed to extract or save JSON: {e}")
