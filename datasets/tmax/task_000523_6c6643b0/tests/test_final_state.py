# test_final_state.py
import os
import subprocess
import pytest
import json

def test_analyze_exfil_script_exists():
    script_path = "/home/user/analyze_exfil.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_exfil_accuracy():
    script_path = "/home/user/analyze_exfil.sh"
    test_data_dir = "/test/data"

    # If the held-out test dataset exists, evaluate against it.
    # Otherwise, evaluate against the primary artifact.
    test_cases = []
    if os.path.isdir(test_data_dir):
        # Assuming a metadata.json exists with the expected tokens for the held-out set
        metadata_path = os.path.join(test_data_dir, "metadata.json")
        if os.path.isfile(metadata_path):
            with open(metadata_path, 'r') as f:
                test_cases = json.load(f)

    if not test_cases:
        # Fallback to testing the primary artifact if held-out set metadata is unavailable
        # In a real grading environment, the expected tokens would be derived or known.
        # Here we ensure the script runs and produces output.
        try:
            out = subprocess.check_output(
                ["bash", script_path, "/app/exfil_video.mp4", "/app/suspicious_service"],
                timeout=120, text=True
            )
            extracted = [line.strip() for line in out.strip().split('\n') if line.strip()]
            assert len(extracted) > 0, "Script failed to extract any tokens from the primary artifact."
        except subprocess.TimeoutExpired:
            pytest.fail("Script execution timed out on the primary artifact.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script execution failed with return code {e.returncode}.")
        return

    correct = 0
    total = sum(len(tc["expected"]) for tc in test_cases)

    assert total > 0, "No expected tokens found in test cases."

    for tc in test_cases:
        try:
            out = subprocess.check_output(
                ["bash", script_path, tc["video"], tc["bin"]],
                timeout=120, text=True
            )
            extracted = [line.strip() for line in out.strip().split('\n') if line.strip()]
            for exp in tc["expected"]:
                if exp in extracted:
                    correct += 1
        except Exception as e:
            print(f"Error processing {tc['video']}: {e}")

    accuracy = correct / total
    assert accuracy >= 0.8, f"Accuracy metric failed: {accuracy:.2f} < 0.8 threshold. Correct: {correct}/{total}"