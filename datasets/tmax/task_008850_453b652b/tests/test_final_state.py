# test_final_state.py
import os
import re

def test_writer_code():
    path = "/home/user/writer.cpp"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "flock(" in content and "LOCK_EX" in content, "File writer.cpp must contain exclusive file lock 'flock(fd, LOCK_EX)'."
    assert "flock(" in content and "LOCK_UN" in content, "File writer.cpp must contain unlock 'flock(fd, LOCK_UN)'."

def test_writer_compiled():
    path = "/home/user/writer"
    assert os.path.isfile(path), f"Compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_results_csv_content():
    path = "/home/user/results.csv"
    assert os.path.isfile(path), f"Results file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 80, f"Expected exactly 80 lines in {path}, found {len(lines)}."

    expected_datasets = {
        "cifar10_full": 0,
        "glue_benchmark": 0,
        "imagenet_subset_1": 0,
        "wikitext_103": 0
    }

    pattern = re.compile(r"^([^,]+),metric=(\d+)$")

    for line in lines:
        match = pattern.match(line)
        assert match, f"Malformed line found in {path}: '{line}'"

        dataset = match.group(1)
        metric = int(match.group(2))

        assert dataset in expected_datasets, f"Unexpected dataset '{dataset}' found in {path}."
        assert 0 <= metric < 20, f"Metric value '{metric}' out of bounds for dataset '{dataset}'."

        expected_datasets[dataset] += 1

    for dataset, count in expected_datasets.items():
        assert count == 20, f"Expected 20 lines for '{dataset}', found {count}."