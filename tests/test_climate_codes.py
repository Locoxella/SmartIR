import glob
import json
import os
import jsonschema
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIMATE_DIR = os.path.join(REPO_ROOT, "codes", "climate")
SCHEMA_PATH = os.path.join(CLIMATE_DIR, "schema.json")

def get_climate_files():
    files = sorted(glob.glob(os.path.join(CLIMATE_DIR, "*.json")))
    return [f for f in files if os.path.basename(f) != "schema.json"]

@pytest.fixture(scope="session")
def climate_schema():
    assert os.path.isfile(SCHEMA_PATH), f"Schema file missing at {SCHEMA_PATH}"
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("file_path", get_climate_files(), ids=lambda p: os.path.basename(p))
def test_climate_code_conforms_to_schema(file_path, climate_schema):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    jsonschema.validate(instance=data, schema=climate_schema)
