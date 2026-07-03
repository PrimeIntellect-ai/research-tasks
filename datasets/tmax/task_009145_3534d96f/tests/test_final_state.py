# test_final_state.py

import os
import subprocess

def test_top2_recommendations_file():
    """Verify that the output file for target_1 exists and has the correct recommendations."""
    output_path = "/home/user/data_pipeline/top2_recommendations.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {output_path}, found {len(lines)}."
    assert lines[0] == "item_E", f"Expected first recommendation to be 'item_E', got '{lines[0]}'."
    assert lines[1] == "item_C", f"Expected second recommendation to be 'item_C', got '{lines[1]}'."

def test_recommend_script_functionality():
    """Verify that the recommend.sh script computes distances and sorts correctly for a different target."""
    script_path = "/home/user/data_pipeline/recommend.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    test_output_path = "/tmp/test_out.txt"

    # Run the script for item_A
    # item_A (12, 19, 32)
    # Distances:
    # item_E (10, 20, 31) -> 2 + 1 + 1 = 4
    # target_1 (10, 20, 30) -> 2 + 1 + 2 = 5
    # item_C (9, 21, 29) -> 3 + 2 + 3 = 8
    # item_D (15, 15, 35) -> 3 + 4 + 3 = 10
    # item_B (100, 200, 300) -> 88 + 181 + 268 = 537

    result = subprocess.run([script_path, "item_A", test_output_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    assert os.path.isfile(test_output_path), "Script did not create the output file."

    with open(test_output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in output, found {len(lines)}."
    assert lines[0] == "item_E", f"Expected first recommendation for item_A to be 'item_E', got '{lines[0]}'."
    assert lines[1] == "target_1", f"Expected second recommendation for item_A to be 'target_1', got '{lines[1]}'."