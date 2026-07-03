# test_final_state.py

import os
import json
import pytest

def test_build_plan_sh():
    build_plan_path = '/home/user/build_plan.sh'
    assert os.path.exists(build_plan_path), f"{build_plan_path} does not exist."

    with open(build_plan_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        '#!/bin/bash',
        'python build_api.py',
        'npm run build'
    ]

    assert lines == expected_lines, f"Contents of {build_plan_path} are incorrect. Got {lines}, expected {expected_lines}."

def test_new_cache_json():
    cache_path = '/home/user/new_cache.json'
    assert os.path.exists(cache_path), f"{cache_path} does not exist."

    with open(cache_path, 'r') as f:
        try:
            cache_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{cache_path} is not a valid JSON file.")

    expected_cache = {
        "utils": "gcc -o utils utils.c",
        "core": "gcc -o core core.c",
        "api": "python build_api.py",
        "frontend": "npm run build",
        "docs": "mkdocs build"
    }

    assert cache_data == expected_cache, f"Contents of {cache_path} are incorrect. Got {cache_data}, expected {expected_cache}."