# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_pipeline_output_files():
    script_path = "/home/user/pipeline.sh"
    ratings_path = "/home/user/ratings.csv"
    train_out = "/home/user/train_features.csv"
    test_out = "/home/user/test_features.csv"

    assert os.path.exists(ratings_path), f"Input file {ratings_path} is missing."

    # Execute the script if the output files don't exist, to be robust
    if not (os.path.exists(train_out) and os.path.exists(test_out)):
        result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
        assert result.returncode == 0, f"Execution of {script_path} failed:\n{result.stderr}"

    assert os.path.exists(train_out), f"Output file {train_out} was not created."
    assert os.path.exists(test_out), f"Output file {test_out} was not created."

    # Compute expected outputs dynamically from ratings.csv
    with open(ratings_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    header = lines[0]
    assert header == "user_id,item_id,rating,timestamp", "Unexpected header in ratings.csv"

    train_rows = []
    test_rows = []

    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) != 4:
            continue
        user_id, item_id, rating_str, timestamp_str = parts
        rating = float(rating_str)
        timestamp = int(timestamp_str)

        if timestamp <= 1620000000:
            train_rows.append((user_id, item_id, rating, timestamp, line))
        else:
            test_rows.append((user_id, item_id, rating, timestamp, line))

    # Calculate means
    train_ratings = [r[2] for r in train_rows]
    global_mean = sum(train_ratings) / len(train_ratings) if train_ratings else 0.0

    item_stats = {}
    for r in train_rows:
        item_id = r[1]
        rating = r[2]
        if item_id not in item_stats:
            item_stats[item_id] = []
        item_stats[item_id].append(rating)

    item_means = {item: sum(ratings)/len(ratings) for item, ratings in item_stats.items()}

    expected_header = header + ",item_mean"

    expected_train_lines = []
    for r in train_rows:
        item_id = r[1]
        mean = item_means[item_id]
        expected_train_lines.append(f"{r[4]},{mean:.2f}")

    expected_test_lines = []
    for r in test_rows:
        item_id = r[1]
        mean = item_means.get(item_id, global_mean)
        expected_test_lines.append(f"{r[4]},{mean:.2f}")

    # Read actual outputs
    with open(train_out, "r") as f:
        actual_train = [line.strip() for line in f if line.strip()]

    with open(test_out, "r") as f:
        actual_test = [line.strip() for line in f if line.strip()]

    assert len(actual_train) > 0, f"{train_out} is empty."
    assert actual_train[0] == expected_header, f"Header in {train_out} is incorrect. Expected: {expected_header}, Got: {actual_train[0]}"

    assert len(actual_test) > 0, f"{test_out} is empty."
    assert actual_test[0] == expected_header, f"Header in {test_out} is incorrect. Expected: {expected_header}, Got: {actual_test[0]}"

    actual_train_set = set(actual_train[1:])
    expected_train_set = set(expected_train_lines)
    assert actual_train_set == expected_train_set, f"Content of {train_out} does not match expected train features."

    actual_test_set = set(actual_test[1:])
    expected_test_set = set(expected_test_lines)
    assert actual_test_set == expected_test_set, f"Content of {test_out} does not match expected test features."