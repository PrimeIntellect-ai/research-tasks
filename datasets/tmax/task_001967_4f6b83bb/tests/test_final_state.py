# test_final_state.py
import os
import shutil
import subprocess
import tempfile
import pytest

def test_yq_fixed():
    """Verify that yq is fixed and installed."""
    try:
        result = subprocess.run(["yq", "--version"], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        pytest.fail("yq executable not found in PATH.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"yq failed to run. It may not be fixed correctly. Stderr: {e.stderr}")

def test_script_exists_and_executable():
    """Verify the ingestion script exists and is executable."""
    script_path = "/home/user/process_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_adversarial_corpus():
    """Verify the script correctly processes clean and evil files."""
    script_path = "/home/user/process_configs.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus dir {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus dir {evil_dir} missing."

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        clean_files = os.listdir(clean_dir)
        evil_files = os.listdir(evil_dir)

        # Copy clean files with a prefix to ensure they are lexicographically first
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(input_dir, f"a_clean_{f}"))

        # Copy evil files with a prefix to ensure they are lexicographically later
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(input_dir, f"z_evil_{f}"))

        # Run the ingestion script
        result = subprocess.run(["bash", script_path, input_dir, output_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

        output_files = set(os.listdir(output_dir))

        bypassed_evil = []
        for f in evil_files:
            if f"z_evil_{f}" in output_files:
                bypassed_evil.append(f)

        modified_clean = []
        for f in clean_files:
            if f"a_clean_{f}" not in output_files:
                modified_clean.append(f)

        errors = []
        if bypassed_evil:
            errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
        if modified_clean:
            errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(modified_clean)}")

        if errors:
            pytest.fail(" | ".join(errors))