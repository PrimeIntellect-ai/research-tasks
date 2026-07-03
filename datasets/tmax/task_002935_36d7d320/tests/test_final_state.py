# test_final_state.py

import os
import time
import shutil
import pytest
import requests

API_URL = "http://127.0.0.1:8000/inventory"
DROPZONE_DIR = "/home/user/dataset/dropzone"
ORGANIZED_DIR = "/home/user/dataset/organized"
TEST_FOLDER_DIR = os.path.join(DROPZONE_DIR, "test_folder")
ORIGINAL_AUDIO = "/app/audio_sample.wav"
DROPPED_AUDIO_1 = os.path.join(TEST_FOLDER_DIR, "audio_sample.wav")
DROPPED_AUDIO_2 = os.path.join(DROPZONE_DIR, "second.wav")

def test_api_and_first_file_processing():
    # Ensure the first file was dropped where expected
    assert os.path.exists(DROPPED_AUDIO_1), f"File {DROPPED_AUDIO_1} is missing. Did you copy it?"

    # Query the API
    try:
        response = requests.get(API_URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {API_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON")

    # Find the category (transcription) for audio_sample.wav
    category = None
    expected_path_suffix = "audio_sample.wav"
    for cat, paths in data.items():
        for p in paths:
            if p.endswith(expected_path_suffix):
                category = cat
                expected_organized_path = p
                break
        if category:
            break

    assert category is not None, "Could not find audio_sample.wav in the /inventory response"

    # Verify the path matches the expected pattern
    expected_path = os.path.join(ORGANIZED_DIR, category, "audio_sample.wav")
    assert expected_organized_path == expected_path, f"Expected path {expected_path}, got {expected_organized_path}"

    # Verify the organized file exists
    assert os.path.exists(expected_path), f"Organized file {expected_path} does not exist"

    # Verify it's a hard link
    stat_drop = os.stat(DROPPED_AUDIO_1)
    stat_org = os.stat(expected_path)
    assert stat_drop.st_ino == stat_org.st_ino, f"File {expected_path} is not a hard link to {DROPPED_AUDIO_1}"

def test_watchdog_processes_new_file():
    # Drop a new file
    shutil.copy(ORIGINAL_AUDIO, DROPPED_AUDIO_2)

    # Wait for the watchdog to process it
    max_retries = 15
    found = False
    category = None

    for _ in range(max_retries):
        time.sleep(1)
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for cat, paths in data.items():
                    for p in paths:
                        if p.endswith("second.wav"):
                            found = True
                            category = cat
                            break
                    if found:
                        break
            if found:
                break
        except requests.RequestException:
            pass

    assert found, "Watchdog did not process the newly dropped file 'second.wav' within the timeout"

    expected_path = os.path.join(ORGANIZED_DIR, category, "second.wav")
    assert os.path.exists(expected_path), f"Organized file {expected_path} does not exist"

    stat_drop = os.stat(DROPPED_AUDIO_2)
    stat_org = os.stat(expected_path)
    assert stat_drop.st_ino == stat_org.st_ino, f"File {expected_path} is not a hard link to {DROPPED_AUDIO_2}"