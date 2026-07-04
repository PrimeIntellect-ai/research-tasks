# test_final_state.py

import os
import json
import csv
import math
import pytest

def compute_expected_distance(csv_path):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0
        a = math.sin(dLat / 2)**2 + math.cos(lat1 * math.pi / 180.0) * math.cos(lat2 * math.pi / 180.0) * math.sin(dLon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    total_dist = 0.0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        prev_lat = None
        prev_lon = None
        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            if prev_lat is not None and prev_lon is not None:
                total_dist += haversine(prev_lat, prev_lon, lat, lon)
            prev_lat = lat
            prev_lon = lon
    return total_dist

def test_fixed_analysis_json_exists():
    path = "/home/user/fixed_analysis.json"
    assert os.path.isfile(path), f"Expected output file {path} to exist."

def test_fixed_analysis_json_content():
    path = "/home/user/fixed_analysis.json"
    assert os.path.isfile(path), f"Expected output file {path} to exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "total_distance_km" in data, "JSON output missing 'total_distance_km' key."

    csv_path = "/home/user/route.csv"
    assert os.path.isfile(csv_path), f"Input data file {csv_path} is missing."

    expected_distance = compute_expected_distance(csv_path)
    actual_distance = data["total_distance_km"]

    assert isinstance(actual_distance, (int, float)), "'total_distance_km' must be a number."

    tolerance = 0.001
    diff = abs(expected_distance - actual_distance)
    assert diff <= tolerance, f"Expected total distance approx {expected_distance:.4f}, but got {actual_distance}. Difference {diff} exceeds tolerance {tolerance}."