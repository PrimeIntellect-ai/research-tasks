# test_final_state.py

import os
import csv
import json
import pytest
import requests
import struct

FRAMES_DIR = "/home/user/frames"
CSV_PATH = "/home/user/distances.csv"
API_URL = "http://127.0.0.1:8000"

def test_frames_extracted():
    assert os.path.exists(FRAMES_DIR), f"Directory {FRAMES_DIR} does not exist"
    frames = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith('.png')])
    assert len(frames) > 0, "No PNG frames found in the frames directory"

    # Check naming convention
    for i, frame in enumerate(frames, start=1):
        expected_name = f"frame_{i:04d}.png"
        assert frame == expected_name, f"Expected frame name {expected_name}, found {frame}"

        frame_path = os.path.join(FRAMES_DIR, frame)
        assert os.path.getsize(frame_path) > 0, f"Frame {frame} is empty"

def test_csv_output():
    assert os.path.exists(CSV_PATH), f"CSV file {CSV_PATH} does not exist"

    with open(CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['start_frame', 'end_frame', 'mad'], f"Incorrect CSV headers: {headers}"

        rows = list(reader)
        assert len(rows) > 0, "CSV file contains no data rows"

        for i, row in enumerate(rows, start=1):
            assert len(row) == 3, f"Row {i} does not have exactly 3 columns"
            assert int(row[0]) == i, f"Expected start_frame {i}, got {row[0]}"
            assert int(row[1]) == i + 1, f"Expected end_frame {i+1}, got {row[1]}"
            try:
                float(row[2])
            except ValueError:
                pytest.fail(f"MAD value '{row[2]}' is not a valid float")

def test_api_distances():
    try:
        response = requests.get(f"{API_URL}/api/distances", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("API response is not valid JSON")

    assert isinstance(data, list), "API response should be a JSON array"
    assert len(data) > 0, "API response array is empty"

    for i, item in enumerate(data, start=1):
        assert 'start_frame' in item, "Missing 'start_frame' in API response"
        assert 'end_frame' in item, "Missing 'end_frame' in API response"
        assert 'mad' in item, "Missing 'mad' in API response"

        assert item['start_frame'] == i, f"Expected start_frame {i}, got {item['start_frame']}"
        assert item['end_frame'] == i + 1, f"Expected end_frame {i+1}, got {item['end_frame']}"
        assert isinstance(item['mad'], (int, float)), f"MAD value {item['mad']} is not a number"

def test_api_frames():
    frame_id = 1
    expected_frame_path = os.path.join(FRAMES_DIR, f"frame_{frame_id:04d}.png")
    assert os.path.exists(expected_frame_path), f"Frame file {expected_frame_path} missing"

    try:
        response = requests.get(f"{API_URL}/api/frames/{frame_id}", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.headers.get('Content-Type') == 'image/png', f"Expected Content-Type image/png, got {response.headers.get('Content-Type')}"

    with open(expected_frame_path, 'rb') as f:
        expected_content = f.read()

    assert response.content == expected_content, "API response content does not match the actual frame file"