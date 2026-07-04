# test_final_state.py
import os
import subprocess
import pytest

PIPELINE_DIR = "/home/user/pipeline"

def test_build_sh_success():
    build_file = os.path.join(PIPELINE_DIR, "build.sh")
    assert os.path.isfile(build_file), f"{build_file} does not exist."

    result = subprocess.run([build_file], capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "BUILD SUCCESS" in result.stdout, "build.sh did not print 'BUILD SUCCESS'."

def test_final_output_matches_golden():
    final_output_file = os.path.join(PIPELINE_DIR, "final_output.csv")
    golden_file = os.path.join(PIPELINE_DIR, "golden.csv")

    assert os.path.isfile(final_output_file), f"File {final_output_file} does not exist."
    assert os.path.isfile(golden_file), f"File {golden_file} does not exist."

    with open(final_output_file, 'r') as f:
        final_content = f.read().strip()

    with open(golden_file, 'r') as f:
        golden_content = f.read().strip()

    assert final_content == golden_content, "final_output.csv does not match golden.csv exactly."

def test_build_sh_precision_fix():
    build_file = os.path.join(PIPELINE_DIR, "build.sh")
    with open(build_file, 'r') as f:
        content = f.read()

    # It shouldn't set precision to 32 anymore.
    assert "NUMPY_PRECISION=32" not in content, "build.sh still contains NUMPY_PRECISION=32."

def test_transform_py_truncation_fix():
    # We test this implicitly by running the script with an input that isn't divisible by batch size
    # and ensuring the output size matches the input size.
    # The golden file has 10 lines, batch size is 3. 10 is not perfectly divisible by 3.
    # If test_final_output_matches_golden passes, the truncation fix is verified.
    # But we can also check the length of the generated output.csv
    output_file = os.path.join(PIPELINE_DIR, "output.csv")
    assert os.path.isfile(output_file), f"{output_file} does not exist."

    with open(output_file, 'r') as f:
        output_lines = [line for line in f if line.strip()]

    assert len(output_lines) == 10, f"Expected 10 lines in output.csv, but got {len(output_lines)}. The truncation bug might not be fully fixed."