# test_final_state.py

import os

def test_minimal_repro_exists():
    repro_path = "/home/user/minimal_repro.py"
    assert os.path.isfile(repro_path), f"The file {repro_path} does not exist. You must create a minimal reproducible example."
    assert os.path.getsize(repro_path) > 0, f"The file {repro_path} is empty."

def test_correct_ids_txt():
    ids_path = "/home/user/correct_ids.txt"
    assert os.path.isfile(ids_path), f"The file {ids_path} does not exist."

    with open(ids_path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 IDs in {ids_path}, but found {len(lines)}."
    assert lines[0] == "2", f"Expected first ID to be '2', but got '{lines[0]}'."
    assert lines[1] == "3", f"Expected second ID to be '3', but got '{lines[1]}'."