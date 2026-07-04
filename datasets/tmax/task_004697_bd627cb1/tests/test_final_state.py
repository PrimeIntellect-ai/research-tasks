# test_final_state.py
import json
import os
import csv
import cv2
import numpy as np

def test_final_summary_json():
    target_file = "/home/user/loc_summary.json"
    assert os.path.exists(target_file), f"Output file {target_file} does not exist."

    with open(target_file, "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {target_file} is not valid JSON."

    # Re-derive expected output
    csv_path = "/home/user/raw_loc_requests.csv"
    expected_screens = {}
    if os.path.exists(csv_path):
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row["translation"] or row["translation"] == "MISSING":
                    continue
                screen = row["screen_id"]
                if screen not in expected_screens:
                    expected_screens[screen] = {"keys": set(), "langs": set()}
                expected_screens[screen]["keys"].add(row["loc_key"])
                expected_screens[screen]["langs"].add(row["lang_target"])

    screens_dict = {}
    for screen, data in expected_screens.items():
        screens_dict[screen] = {
            "unique_keys": len(data["keys"]),
            "languages_covered": sorted(list(data["langs"]))
        }

    video_path = '/app/ui_test.mp4'
    screen_loads = 0
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Check if 10x10 top-left is pure white
            if np.array_equal(frame[0:10, 0:10], np.full((10, 10, 3), 255, dtype=np.uint8)):
                screen_loads += 1
        cap.release()

    expected = {
        "total_screen_loads_from_video": screen_loads,
        "screens": screens_dict
    }

    # Metric computation
    accuracy = 1.0 if agent_data == expected else 0.0

    assert accuracy >= 1.0, f"accuracy={accuracy} is below threshold 1.0. Expected {expected}, got {agent_data}"