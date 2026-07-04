# test_final_state.py

import os
import stat
import math

def test_recommend_script_exists_and_executable():
    script_path = "/home/user/analysis/recommend.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_invalid_rows_log():
    log_path = "/home/user/analysis/invalid_rows.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_invalid_rows = {
        "U4,0.5,1.2,3.4,0.1,extra_col",
        "invalid_id,1.0,1.0,1.0,1.0",
        "U6,abc,1.1,3.3,0.2",
        "U9,0.5"
    }

    actual_invalid_rows = set(lines)

    missing = expected_invalid_rows - actual_invalid_rows
    extra = actual_invalid_rows - expected_invalid_rows

    assert not missing, f"Missing expected invalid rows in log: {missing}"
    assert not extra, f"Found unexpected invalid rows in log: {extra}"

def test_recommendations_txt():
    rec_path = "/home/user/analysis/recommendations.txt"
    assert os.path.isfile(rec_path), f"{rec_path} does not exist."

    with open(rec_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 recommendations, found {len(lines)}."

    # Parse the lines
    recommendations = []
    for line in lines:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid format in recommendations.txt: {line}"
        user_id, distance_str = parts
        try:
            distance = float(distance_str)
        except ValueError:
            assert False, f"Distance is not a valid float: {distance_str}"
        recommendations.append((user_id, distance_str))

    # Expected:
    # U10, 0.100
    # U2, 0.200
    # U5, 0.200

    assert recommendations[0] == ("U10", "0.100"), f"First recommendation should be U10,0.100, got {recommendations[0][0]},{recommendations[0][1]}"

    # U2 and U5 can be in any order since they have the same distance
    second_and_third = {recommendations[1], recommendations[2]}
    expected_second_and_third = {("U2", "0.200"), ("U5", "0.200")}

    assert second_and_third == expected_second_and_third, f"Expected second and third recommendations to be U2 and U5 with distance 0.200, got {second_and_third}"