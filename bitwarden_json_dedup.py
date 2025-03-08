#!/usr/bin/env python3

import json
import copy
import sys
import os
from typing import Dict, List, Any


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize an item by removing fields we want to ignore when comparing items.
    Returns a deep copy with ignored fields removed.
    """
    # Create a deep copy to avoid modifying the original
    normalized = copy.deepcopy(item)

    # Remove the fields we want to ignore for comparison
    fields_to_ignore = [
        "lastUsedDate",
        "revisionDate",
        "creationDate",
        "deletedDate",
        "folderId",
        "collectionIds",
        "id",
    ]

    # Remove top-level fields
    for field in fields_to_ignore:
        if field in normalized:
            del normalized[field]

    # Handle passwordHistory separately as it may contain lastUsedDate
    if "passwordHistory" in normalized and normalized["passwordHistory"]:
        for history_item in normalized["passwordHistory"]:
            if "lastUsedDate" in history_item:
                del history_item["lastUsedDate"]

    return normalized


def deduplicate_items(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove duplicate items from the Bitwarden export JSON data while ignoring specified fields.
    """
    if "items" not in data or not isinstance(data["items"], list):
        return data

    # Create a new result with everything except items
    result = {k: v for k, v in data.items() if k != "items"}
    result["items"] = []

    # Use a set to track normalized items we've seen
    seen_items = set()

    for item in data["items"]:
        # Normalize the item for comparison
        normalized = normalize_item(item)

        # Convert to a hashable format (JSON string)
        item_str = json.dumps(normalized, sort_keys=True)

        # If we haven't seen this normalized item, add the original to results
        if item_str not in seen_items:
            seen_items.add(item_str)
            result["items"].append(item)

    # Sort the items first by name, then by id
    result["items"].sort(key=lambda x: (x.get("name", ""), x.get("id", "")))

    return result


def main():
    # Check if input file was provided
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} input_file.json [output_file.json]")
        sys.exit(1)

    # Get input file path from command line
    input_file = sys.argv[1]

    # Determine output file path
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Create default output filename based on input filename
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_dedup.json"

    try:
        # Read the JSON file
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Deduplicate the items
        deduped_data = deduplicate_items(data)

        # Write the result back to the output file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(deduped_data, file, indent=2, ensure_ascii=False)

        print(f"Original item count: {len(data['items'])}")
        print(f"Deduplicated item count: {len(deduped_data['items'])}")
        print(
            f"Removed {len(data['items']) - len(deduped_data['items'])} duplicate items"
        )
        print(f"Deduplicated data written to {output_file}")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
    except json.JSONDecodeError:
        print(f"Error: File {input_file} contains invalid JSON")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
