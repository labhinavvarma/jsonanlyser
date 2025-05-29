import json
from pathlib import Path
from typing import List, Dict, Any

def is_flat_value(val: Any) -> bool:
    """Check if value is a primitive (not dict/list)."""
    return val is None or isinstance(val, (int, float, str, bool))

def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON and filter to only dict entries."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON must be an array of objects.")
        return [item for item in data if isinstance(item, dict)]

def find_strict_common_flat_keys(data: List[Dict[str, Any]]) -> List[str]:
    """Find keys common to all rows with flat (non-nested, non-null) values."""
    keys = set(data[0].keys())
    for row in data:
        keys &= {
            k for k, v in row.items()
            if v is not None and is_flat_value(v)
        }
    return list(keys)

def filter_data(data: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    """Keep only specified keys from each row."""
    return [{k: row[k] for k in keys} for row in data]

def save_json(data: List[Dict[str, Any]], out_path: str):
    """Save cleaned data to file."""
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clean_json_file_strict(input_path: str, output_path: str):
    print(f"📂 Reading from: {input_path}")
    raw_data = load_json(input_path)
    common_keys = find_strict_common_flat_keys(raw_data)
    print(f"🔍 Keeping columns: {common_keys}")
    cleaned = filter_data(raw_data, common_keys)
    save_json(cleaned, output_path)
    print(f"✅ Cleaned JSON saved to: {output_path}")

# --- Example usage ---
if __name__ == "__main__":
    input_file = "your_input.json"       # Replace with your real file
    output_file = "cleaned_output.json"
    clean_json_file_strict(input_file, output_file)
