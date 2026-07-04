# test_final_state.py
import os
import json
import pytest

def parse_semver(version_str):
    """Helper to parse semantic version string into a tuple of integers."""
    return tuple(int(part) for part in version_str.split('.'))

def test_updates_json_correct():
    current_path = "/home/user/api-version-resolver/current.json"
    wanted_path = "/home/user/api-version-resolver/wanted.json"
    updates_path = "/home/user/updates.json"

    assert os.path.exists(current_path), f"File {current_path} is missing."
    assert os.path.exists(wanted_path), f"File {wanted_path} is missing."
    assert os.path.exists(updates_path), f"File {updates_path} is missing. Did you save the curl output?"

    with open(current_path, "r") as f:
        current_data = json.load(f)

    with open(wanted_path, "r") as f:
        wanted_data = json.load(f)

    # Dynamically compute expected updates based on SemVer rules
    expected_updates = []
    for pkg, curr_ver in current_data.items():
        if pkg in wanted_data:
            want_ver = wanted_data[pkg]
            if parse_semver(want_ver) > parse_semver(curr_ver):
                expected_updates.append({
                    "package": pkg,
                    "from": curr_ver,
                    "to": want_ver
                })

    # The output MUST be sorted alphabetically by package name
    expected_updates.sort(key=lambda x: x["package"])

    with open(updates_path, "r") as f:
        try:
            actual_updates = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {updates_path} does not contain valid JSON.")

    assert isinstance(actual_updates, list), f"The JSON in {updates_path} must be an array."
    assert actual_updates == expected_updates, (
        f"The contents of {updates_path} do not match the expected updates. "
        f"Expected: {expected_updates}, Actual: {actual_updates}"
    )