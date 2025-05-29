import json
import re
from typing import List, Dict, Any
from pathlib import Path

def is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float))

def is_alphanumeric_code(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[A-Z]{2,}[0-9]{2,}", value.strip())

def is_clean_value(value: Any) -> bool:
    return is_numeric(value) or is_alphanumeric_code(value)

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Load and validate that the input is a JSON array of dictionaries."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array at the top level.")
    return [row for row in data if isinstance(row, dict)]

def find_consistent_clean_keys(data: List[Dict[str, Any]]) -> List[str]:
    """Keep keys that exist in every record and have clean values in all rows."""
    if not data:
        return []

    common_keys = set(data[0].keys())
    for row in data:
        common_keys &= row.keys()

    valid_keys = []
    for key in common_keys:
        values = [row.get(key) for row in data]
        if all(is_clean_value(val) for val in values):
            valid_keys.append(key)

    return valid_keys

def filter_data(data: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    return [{k: row[k] for k in keys} for row in data]

def save_json(data: List[Dict[str, Any]], out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def process_and_clean_json(input_path: str, output_path: str):
    print(f"📥 Loading: {input_path}")
    data = load_json_file(input_path)
    print(f"🔍 Total records: {len(data)}")

    valid_keys = find_consistent_clean_keys(data)
    print(f"✅ Keeping columns: {valid_keys}")

    cleaned_data = filter_data(data, valid_keys)
    save_json(cleaned_data, output_path)
    print(f"✅ Cleaned JSON saved to: {output_path}")

# --- Example usage ---
if __name__ == "__main__":
    input_file = "messy_input.json"             # Replace with your file
    output_file = "cleaned_output.json"         # Output file
    process_and_clean_json(input_file, output_file)
