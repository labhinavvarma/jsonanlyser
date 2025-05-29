import json
import os
from uuid import uuid4
from typing import Any
from pathlib import Path

def load_json_file(filepath: str) -> Any:
    """Loads a JSON file from disk."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def flatten_payload(payload: Any) -> Any:
    """
    Attempts to extract meaningful 'data' from a payload.

    - If 'data' exists at top level, it returns that.
    - Else, it returns the first list/dict-like value it can find.
    """
    if isinstance(payload, dict):
        if "data" in payload:
            return payload["data"]

        # Fallback: return first list or dict value
        for key, val in payload.items():
            if isinstance(val, (list, dict)):
                return val

    raise ValueError("No usable data found in the uploaded file.")

def save_json(data: Any, output_dir: str = ".", prefix: str = "cleaned") -> str:
    """Saves the data to a new JSON file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{uuid4().hex[:8]}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return filepath

def process_uploaded_file(input_path: str, output_dir: str = "json_outputs") -> str:
    """
    Main function:
    - Loads the uploaded file
    - Extracts meaningful data
    - Saves it to a new file
    - Returns new file path
    """
    print(f"📥 Processing uploaded file: {input_path}")
    payload = load_json_file(input_path)
    data = flatten_payload(payload)
    output_path = save_json(data, output_dir=output_dir)
    print(f"✅ Cleaned data saved to: {output_path}")
    return output_path

# --- Example Usage ---
if __name__ == "__main__":
    # Replace this with the path to your uploaded payload JSON file
    uploaded_file_path = "uploaded_payload.json"  # 🔁 <-- Put your file here

    try:
        final_path = process_uploaded_file(uploaded_file_path)
    except Exception as e:
        print(f"❌ Error: {e}")
