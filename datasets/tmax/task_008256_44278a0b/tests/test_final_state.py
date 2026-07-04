# test_final_state.py

import os
import json
import pytest

def test_capacity_review_directory():
    assert os.path.isdir("/home/user/capacity_review"), "/home/user/capacity_review directory does not exist."

def test_report_json():
    report_path = "/home/user/capacity_review/report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert "projects" in data, "JSON report missing 'projects' key."
    projects = data["projects"]

    # Expected order and sizes (based on initial setup)
    expected_projects = [
        {"name": "proj_gamma", "size_bytes": 100 * 1024 * 1024},
        {"name": "proj_alpha", "size_bytes": 50 * 1024 * 1024},
        {"name": "proj_beta", "size_bytes": 10 * 1024 * 1024},
        {"name": "proj_delta", "size_bytes": 5 * 1024 * 1024},
    ]

    assert len(projects) == len(expected_projects), f"Expected {len(expected_projects)} projects in report, found {len(projects)}."

    for i, expected in enumerate(expected_projects):
        assert projects[i]["name"] == expected["name"], f"Expected rank {i+1} to be {expected['name']}, got {projects[i].get('name')}."
        # Use >= expected size because directory itself might take a few bytes
        assert projects[i]["size_bytes"] >= expected["size_bytes"], f"Size for {expected['name']} is too small."

def test_symlinks():
    link1 = "/home/user/capacity_review/rank_1_proj_gamma"
    link2 = "/home/user/capacity_review/rank_2_proj_alpha"

    assert os.path.islink(link1), f"{link1} is not a symlink."
    assert os.path.islink(link2), f"{link2} is not a symlink."

    target1 = os.readlink(link1)
    target2 = os.readlink(link2)

    assert target1 == "../projects/proj_gamma", f"Symlink {link1} does not point to correct relative path. Got {target1}."
    assert target2 == "../projects/proj_alpha", f"Symlink {link2} does not point to correct relative path. Got {target2}."

def test_profile_env_var():
    profile_path = "/home/user/.profile"
    assert os.path.isfile(profile_path), f"{profile_path} does not exist."

    with open(profile_path, 'r') as f:
        content = f.read()

    expected_str = 'export CAPACITY_REVIEW_DIR="/home/user/capacity_review"'
    count = content.count(expected_str)

    assert count >= 1, f"{profile_path} does not contain the expected export statement."
    assert count == 1, f"{profile_path} contains the export statement multiple times (not idempotent)."

def test_pipeline_script():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."