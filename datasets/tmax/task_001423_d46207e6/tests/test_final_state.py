# test_final_state.py

import os
import subprocess
import csv
import math

DIR_PATH = "/home/user/etl_pipeline"
MAKEFILE_PATH = os.path.join(DIR_PATH, "Makefile")
MATCH_PY_PATH = os.path.join(DIR_PATH, "match.py")
SOURCE_A_PATH = os.path.join(DIR_PATH, "source_A.csv")
SOURCE_B_JSON_PATH = os.path.join(DIR_PATH, "source_B.json")
SOURCE_B_NORM_PATH = os.path.join(DIR_PATH, "source_B_norm.csv")
MATCHES_PATH = os.path.join(DIR_PATH, "matches.csv")


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def test_makefile_exists():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile not found at {MAKEFILE_PATH}"


def test_match_py_exists():
    assert os.path.isfile(MATCH_PY_PATH), f"match.py not found at {MATCH_PY_PATH}"


def test_make_execution_and_outputs():
    # Remove outputs to test Makefile execution from scratch
    if os.path.exists(SOURCE_B_NORM_PATH):
        os.remove(SOURCE_B_NORM_PATH)
    if os.path.exists(MATCHES_PATH):
        os.remove(MATCHES_PATH)

    # Run make all
    result = subprocess.run(["make", "all"], cwd=DIR_PATH, capture_output=True, text=True)
    assert result.returncode == 0, f"'make all' failed with output:\n{result.stderr}\n{result.stdout}"

    assert os.path.isfile(SOURCE_B_NORM_PATH), f"make did not generate {SOURCE_B_NORM_PATH}"
    assert os.path.isfile(MATCHES_PATH), f"make did not generate {MATCHES_PATH}"


def test_source_b_norm_content():
    # Ensure source_B_norm.csv has correct header and data
    with open(SOURCE_B_NORM_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{SOURCE_B_NORM_PATH} is empty"
    assert rows[0] == ["id", "lat", "lon"], f"Incorrect header in {SOURCE_B_NORM_PATH}: {rows[0]}"

    # Check that B1, B2, B3, B4 are present with correct coords
    data_dict = {row[0]: (float(row[1]), float(row[2])) for row in rows[1:]}
    assert "B1" in data_dict
    assert math.isclose(data_dict["B1"][0], 40.7306)
    assert math.isclose(data_dict["B1"][1], -73.9866)


def test_matches_content():
    # Recompute expected matches
    source_A = [
        ("A1", 40.7128, -74.0060),
        ("A2", 34.0522, -118.2437),
        ("A3", 41.8781, -87.6298),
        ("A4", 48.8566, 2.3522)
    ]
    source_B = [
        ("B1", 40.7306, -73.9866),
        ("B2", 34.0500, -118.2500),
        ("B3", 51.5074, -0.1278),
        ("B4", 48.8584, 2.3508)
    ]

    expected_matches = []
    for a_id, a_lat, a_lon in source_A:
        for b_id, b_lat, b_lon in source_B:
            dist = haversine(a_lat, a_lon, b_lat, b_lon)
            if dist <= 5.0:
                expected_matches.append((a_id, b_id, round(dist, 2)))

    expected_matches.sort(key=lambda x: (x[0], x[1]))

    with open(MATCHES_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{MATCHES_PATH} is empty"
    assert rows[0] == ["id_A", "id_B", "distance_km"], f"Incorrect header in {MATCHES_PATH}: {rows[0]}"

    actual_matches = []
    for row in rows[1:]:
        assert len(row) == 3, f"Invalid row format in {MATCHES_PATH}: {row}"
        actual_matches.append((row[0], row[1], float(row[2])))

    assert actual_matches == expected_matches, f"Matches mismatch. Expected {expected_matches}, got {actual_matches}"


def test_makefile_dag():
    # Test if DAG is correctly defined using make -n
    # Touching source_B.json should trigger normalize and match
    os.utime(SOURCE_B_JSON_PATH, None)
    result = subprocess.run(["make", "-n", "all"], cwd=DIR_PATH, capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout.lower() + result.stderr.lower()

    # Check if normalize or the output file is mentioned
    assert "source_b_norm" in output or "normalize" in output, "Makefile DAG does not trigger normalize when source_B.json changes"
    assert "match" in output or "matches.csv" in output, "Makefile DAG does not trigger match when source_B.json changes"