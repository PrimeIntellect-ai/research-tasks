# test_final_state.py

import os
import json
import pytest

def test_scripts_exist():
    expected_scripts = [
        "/home/user/step1_parse.py",
        "/home/user/step2_sort_group.py",
        "/home/user/step3_stats.py"
    ]
    for script in expected_scripts:
        assert os.path.exists(script), f"Expected script {script} is missing."
        assert os.path.isfile(script), f"{script} is not a file."

def test_makefile_exists_and_targets():
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), "Makefile is missing."
    assert os.path.isfile(makefile_path), "Makefile is not a file."

    with open(makefile_path, "r", encoding="utf-8") as f:
        content = f.read()

    targets = ["parse", "group", "stats", "all", "clean"]
    for target in targets:
        # A simple check for target definition in Makefile
        assert f"{target}:" in content, f"Target '{target}' is missing from the Makefile."

def test_rolling_stats_exists_and_correct():
    stats_path = "/home/user/rolling_stats.json"
    assert os.path.exists(stats_path), f"{stats_path} is missing."
    assert os.path.isfile(stats_path), f"{stats_path} is not a file."

    with open(stats_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{stats_path} is not valid JSON.")

    assert isinstance(data, dict), f"Expected {stats_path} to contain a JSON object."

    assert "S1" in data, "Session S1 is missing from rolling_stats.json."
    assert "S2" in data, "Session S2 is missing from rolling_stats.json."

    s1_stat = data.get("S1")
    s2_stat = data.get("S2")

    assert isinstance(s1_stat, (int, float)), f"S1 stat must be a number, got {type(s1_stat)}."
    assert isinstance(s2_stat, (int, float)), f"S2 stat must be a number, got {type(s2_stat)}."

    assert abs(s1_stat - 200.0) < 0.01, f"S1 stat is incorrect. Expected ~200.0, got {s1_stat}."
    assert abs(s2_stat - 70.0) < 0.01, f"S2 stat is incorrect. Expected ~70.0, got {s2_stat}."

    assert "" not in data, "Empty session ID was not filtered out."
    assert None not in data, "Null session ID was not filtered out."