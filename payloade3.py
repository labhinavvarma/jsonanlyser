import json
from pathlib import Path
from typing import List, Dict, Any
import re

def is_numeric(val: Any) -> bool:
    return isinstance(val, (int, float))

def is_alphanumeric_code(val: Any) -> bool:
    return isinstance(val, str) and re.fullmatch(r"[A-Z]{2,}[0-9]{2,}", val.strip())

def load_json(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of objects.")
        return [row for row in data if isinstance(row, dict)]

def find_valid_columns(data: List[Dict[str, Any]]) -> List[str]:
    if not data:
        return []
    
    common_keys = set(data[0].keys())
    for row in data:
        common_keys &= row.keys()

    valid_keys = []
    for key in common_keys:
        values = [row[key] for row in data]
        if all(is_numeric(v) for v in values) or all(is_alphanumeric_code(v) for v in values):
            valid_keys.append(key)

    return valid_keys

def filter_data(data: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    return [{k: row[k] for k in keys} for row in data]

def save_json(data: List[Dict[str, Any]], out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clean_json_numeric_and_code_fields(input_path: str, output_path: str):
    data = load_json(input_path)
    valid_columns = find_valid_columns(data)
    cleaned = filter_data(data, valid_columns)
    save_json(cleaned, output_path)
    print(f"✅ Cleaned JSON saved to: {output_path}")
    print(f"🔢 Retained columns: {valid_columns}")

# Example usage
if __name__ == "__main__":
    input_file = "your_input.json"              # Replace with your actual file
    output_file = "cleaned_numeric_codes.json"  # Output file
    clean_json_numeric_and_code_fields(input_file, output_file)
