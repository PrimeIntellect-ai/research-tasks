# test_final_state.py

import os
import subprocess
import json
import tempfile
import shutil
import pytest

def test_libmatrix_built():
    """Verify that the C library was successfully built and exports the correct symbol."""
    so_path = "/app/vendored/c_matrix_lib-1.0/libmatrix.so"
    assert os.path.exists(so_path), f"Shared library not built: {so_path}"

    try:
        nm_out = subprocess.check_output(["nm", "-D", so_path], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {so_path}: {e}")

    assert "calculate_determinant" in nm_out, "calculate_determinant symbol not found in libmatrix.so"

def test_sanitizer_adversarial_corpus():
    """Run the sanitizer against the adversarial corpus and verify the results."""
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Sanitizer script missing: {sanitizer_path}"

    evil_dir = "/app/tests/corpus/evil"
    clean_dir = "/app/tests/corpus/clean"

    assert os.path.exists(evil_dir), f"Evil corpus missing: {evil_dir}"
    assert os.path.exists(clean_dir), f"Clean corpus missing: {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        os.makedirs(input_dir)

        # Copy all corpus files into a single input directory for the tool
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(input_dir, f))
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(input_dir, f))

        output_json = os.path.join(tmpdir, "output.json")

        try:
            subprocess.run(
                ["python3", sanitizer_path, input_dir, output_json],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"sanitizer.py failed to execute:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

        assert os.path.exists(output_json), f"Output JSON not created at {output_json}"

        try:
            with open(output_json, "r") as f:
                results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

        evil_bypassed = []
        for ef in evil_files:
            if results.get(ef) != "reject":
                evil_bypassed.append(ef)

        clean_modified = []
        for cf in clean_files:
            if results.get(cf) != "accept":
                clean_modified.append(cf)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))