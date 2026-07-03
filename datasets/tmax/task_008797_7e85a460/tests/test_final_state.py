# test_final_state.py
import os
import json
import stat

def test_top_datasets():
    """Test that the top_datasets.json contains the correct top 2 datasets."""
    path = "/home/user/top_datasets.json"
    assert os.path.exists(path), f"File {path} does not exist. Did you run Phase 1?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    assert isinstance(data, list), f"{path} must contain a JSON array."
    assert set(data) == {"d2", "d4"}, f"Expected top datasets to be {{'d2', 'd4'}}, got {set(data)}"

def test_final_pairs():
    """Test that final_pairs.json contains the correct knowledge graph pattern matches."""
    path = "/home/user/final_pairs.json"
    assert os.path.exists(path), f"File {path} does not exist. Did you run the full pipeline?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    assert isinstance(data, list), f"{path} must contain a JSON array."

    expected_pairs = [
        {"source_dataset": "d2", "target_dataset": "d4"},
        {"source_dataset": "d4", "target_dataset": "d2"}
    ]

    assert len(data) == 2, f"Expected exactly 2 pairs in {path}, got {len(data)}"

    for expected in expected_pairs:
        assert expected in data, f"Missing expected pair {expected} in {path}"

def test_run_pipeline_script_exists_and_executable():
    """Test that the bash wrapper script exists and is executable."""
    path = "/home/user/run_pipeline.sh"
    assert os.path.exists(path), f"Script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."