# test_final_state.py

import os
import json
import base64
import pytest

MANIFEST_PATH = "/home/user/deploy_manifest.json"
ROSTER_PATH = "/home/user/roster.json"

def test_roster_exists():
    assert os.path.isfile(ROSTER_PATH), f"The output file {ROSTER_PATH} does not exist. Did you run your Go program?"

def test_roster_content():
    assert os.path.isfile(MANIFEST_PATH), f"The input file {MANIFEST_PATH} is missing."

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {MANIFEST_PATH} is not valid JSON.")

    allowed_regions = set(manifest.get("global_allowed_regions", []))
    services = manifest.get("services", [])

    expected_roster = []
    for service in services:
        region = service.get("target_region")
        mem_limit = service.get("memory_limit_mb", 0)
        req_mem = service.get("required_memory_mb", 0)

        if region in allowed_regions and mem_limit >= req_mem:
            name = service.get("name", "")
            version = service.get("version", "")

            raw_token = f"{name}:{version}".encode('utf-8')
            encoded_token = base64.b32encode(raw_token).decode('utf-8').rstrip('=')

            expected_roster.append({
                "service": name,
                "token": encoded_token
            })

    expected_roster.sort(key=lambda x: x["service"])

    with open(ROSTER_PATH, 'r') as f:
        try:
            actual_roster = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {ROSTER_PATH} is not valid JSON.")

    assert isinstance(actual_roster, list), f"Expected {ROSTER_PATH} to contain a JSON array."
    assert len(actual_roster) == len(expected_roster), f"Expected {len(expected_roster)} services in roster, found {len(actual_roster)}."

    for i in range(len(expected_roster)):
        expected = expected_roster[i]
        actual = actual_roster[i]

        assert actual.get("service") == expected["service"], f"Expected service name '{expected['service']}' at index {i}, but got '{actual.get('service')}'."
        assert actual.get("token") == expected["token"], f"Expected token '{expected['token']}' for service '{expected['service']}', but got '{actual.get('token')}'."