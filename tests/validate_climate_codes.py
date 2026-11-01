#!/usr/bin/env python3
"""Validate all climate code JSON files against schema.json."""

import glob
import json
import os
import sys

def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    climate_dir = os.path.join(repo_root, "codes", "climate")
    schema_path = os.path.join(climate_dir, "schema.json")

    if not os.path.isfile(schema_path):
        print(f"Error: Schema not found at {schema_path}", file=sys.stderr)
        return 1

    try:
        import jsonschema
    except ImportError:
        print("Error: 'jsonschema' package is required. Install with: pip install jsonschema", file=sys.stderr)
        return 1

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    json_files = sorted(glob.glob(os.path.join(climate_dir, "*.json")))
    target_files = [f for f in json_files if os.path.basename(f) != "schema.json"]

    if not target_files:
        print(f"Error: No climate code JSON files found in {climate_dir}", file=sys.stderr)
        return 1

    valid_count = 0
    errors = []

    for file_path in target_files:
        rel_path = os.path.relpath(file_path, repo_root)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            errors.append((rel_path, f"JSON Syntax Error: {e}"))
            continue

        try:
            jsonschema.validate(instance=data, schema=schema)
            valid_count += 1
        except jsonschema.exceptions.ValidationError as e:
            errors.append((rel_path, f"Schema Validation Error: {e.message} (path: {'/'.join(str(p) for p in e.path)})"))
        except Exception as e:
            errors.append((rel_path, f"Validation Error: {e}"))

    total = len(target_files)
    print(f"Validated {total} climate code files against schema.json:")
    print(f"  Passed: {valid_count}/{total}")

    if errors:
        print(f"\n  Failed: {len(errors)}/{total}", file=sys.stderr)
        for path, err in errors:
            print(f"    - {path}: {err}", file=sys.stderr)
        return 1

    print("All climate code files are valid!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
