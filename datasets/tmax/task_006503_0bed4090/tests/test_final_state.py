# test_final_state.py
import os
import subprocess
import tempfile
import shutil

def test_actual_results_exists_and_correct():
    actual_path = "/home/user/actual_results.txt"
    assert os.path.isfile(actual_path), f"File {actual_path} does not exist."

    expected_content = """01 20
02 42
03 12
04 35
05 300
06 81
07 55
08 8
09 155
10 75
11 121
12 40
13 50
14 64
15 50
16 9
17 39
18 100
19 200
20 125"""

    with open(actual_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, "The contents of actual_results.txt do not match the expected mathematical calculations."

def test_patch_file_exists_and_applies_correctly():
    patch_path = "/home/user/api_math.patch"
    expected_path = "/home/user/expected_results.txt"
    actual_path = "/home/user/actual_results.txt"

    assert os.path.isfile(patch_path), f"File {patch_path} does not exist."
    assert os.path.isfile(expected_path), f"File {expected_path} does not exist."
    assert os.path.isfile(actual_path), f"File {actual_path} does not exist."

    # Create a temporary directory to safely apply the patch
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_expected = os.path.join(tmpdir, "expected_results.txt")
        shutil.copy(expected_path, tmp_expected)

        # Apply the patch
        try:
            subprocess.run(
                ["patch", tmp_expected, patch_path],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            assert False, f"Failed to apply patch {patch_path} to {expected_path}. Error: {e.stderr}"

        # Read the patched file
        with open(tmp_expected, "r") as f:
            patched_content = f.read().strip()

        # Read the actual results file
        with open(actual_path, "r") as f:
            actual_content = f.read().strip()

        assert patched_content == actual_content, "Applying the patch to expected_results.txt did not produce the contents of actual_results.txt."

def test_patch_contains_unified_diff_format():
    patch_path = "/home/user/api_math.patch"
    assert os.path.isfile(patch_path), f"File {patch_path} does not exist."

    with open(patch_path, "r") as f:
        patch_content = f.read()

    assert "---" in patch_content and "+++" in patch_content, "The patch file does not appear to be in unified diff format."
    assert "-06 80" in patch_content, "The patch is missing the removal of the incorrect line for ID 06."
    assert "+06 81" in patch_content, "The patch is missing the addition of the correct line for ID 06."
    assert "-18 99" in patch_content, "The patch is missing the removal of the incorrect line for ID 18."
    assert "+18 100" in patch_content, "The patch is missing the addition of the correct line for ID 18."