# test_final_state.py

import os
import subprocess
import pytest
import glob

APP_DIR = "/home/user/app"
CLEAN_CORPUS_DIR = os.path.join(APP_DIR, "clean_corpus")
EVIL_CORPUS_DIR = os.path.join(APP_DIR, "evil_corpus")
FILTER_SERVICE_DIR = os.path.join(APP_DIR, "filter_service")
VERIFIER_SCRIPT = os.path.join(APP_DIR, "verifier.py")

def test_rust_project_exists():
    assert os.path.isdir(FILTER_SERVICE_DIR), f"Rust project directory missing: {FILTER_SERVICE_DIR}"
    cargo_toml = os.path.join(FILTER_SERVICE_DIR, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing in {FILTER_SERVICE_DIR}"
    main_rs = os.path.join(FILTER_SERVICE_DIR, "src", "main.rs")
    assert os.path.isfile(main_rs), f"main.rs missing in {FILTER_SERVICE_DIR}/src/"

def test_verifier_script_passes():
    """
    Runs the verifier script which spawns the emitter and sink, runs the agent's binary,
    and asserts the correct analytical output for clean files and the absence of output for evil files.
    """
    assert os.path.isfile(VERIFIER_SCRIPT), f"Verifier script missing: {VERIFIER_SCRIPT}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean CSV files found."
    assert len(evil_files) > 0, "No evil CSV files found."

    try:
        result = subprocess.run(
            ["python3", VERIFIER_SCRIPT],
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Verifier script timed out after 60 seconds.")

    if result.returncode != 0:
        # The verifier script failed. We surface the output which contains the summary.
        pytest.fail(f"Verifier script failed with return code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}")