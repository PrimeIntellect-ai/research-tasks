# test_final_state.py

import os
import pytest

def test_index_csv_exists_and_content():
    index_path = "/home/user/doc_repo/index.csv"
    assert os.path.isfile(index_path), f"File {index_path} does not exist. Did the script run and create it?"

    expected_content = (
        "Model,MaxTemp,TotalLayers\n"
        "Benchy,215,315\n"
        "CalibCube,200,50\n"
        "VoronPart,255,150"
    )

    with open(index_path, 'r') as f:
        actual_content = f.read().strip()

    # Replace Windows line endings if present
    actual_content = actual_content.replace('\r\n', '\n')

    assert actual_content == expected_content, (
        f"Content of {index_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_script_uses_atomic_write():
    script_path = "/home/user/build_index.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for atomic write indicators
    atomic_indicators = ['os.replace', 'os.rename', 'shutil.move', '.replace(', '.rename(']
    has_atomic = any(indicator in content for indicator in atomic_indicators)
    assert has_atomic, (
        f"Script {script_path} does not appear to use an atomic write. "
        "You must write to a temporary file and rename/replace it."
    )