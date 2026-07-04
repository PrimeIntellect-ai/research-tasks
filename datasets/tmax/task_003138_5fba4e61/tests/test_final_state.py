# test_final_state.py

import os
import json
import subprocess
import tempfile

def test_setup_py_fixed():
    """Test that setup.py has been fixed to allow installation."""
    setup_path = "/app/phys_fit-1.2.0/setup.py"
    assert os.path.isfile(setup_path), f"{setup_path} is missing"

    with open(setup_path, 'r') as f:
        content = f.read()

    # Simple heuristic to check if the missing comma bug was fixed
    stripped = content.replace(" ", "").replace("'", "").replace('"', '')
    assert "numpyscipy" not in stripped, "setup.py still contains the missing comma bug causing 'numpyscipy'"

def test_venv_and_package_installed():
    """Test that the virtual environment exists and phys_fit is installed."""
    python_path = "/home/user/venv/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python not found at {python_path}"

    # Check if phys_fit is importable in the venv
    result = subprocess.run(
        [python_path, "-c", "import phys_fit.oscillator"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to import phys_fit in the venv. Did you install it?\nStderr: {result.stderr}"

def test_classify_sims_script():
    """Test the anomaly detector script against the adversarial corpora."""
    script_path = "/home/user/classify_sims.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    python_path = "/home/user/venv/bin/python"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"

    with tempfile.TemporaryDirectory() as tmpdir:
        clean_json = os.path.join(tmpdir, "clean.json")
        evil_json = os.path.join(tmpdir, "evil.json")

        # Run on clean corpus
        res_clean = subprocess.run([
            python_path, script_path,
            "--input-dir", clean_dir,
            "--output-json", clean_json
        ], capture_output=True, text=True)
        assert res_clean.returncode == 0, f"classify_sims.py failed on clean corpus:\n{res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run([
            python_path, script_path,
            "--input-dir", evil_dir,
            "--output-json", evil_json
        ], capture_output=True, text=True)
        assert res_evil.returncode == 0, f"classify_sims.py failed on evil corpus:\n{res_evil.stderr}"

        assert os.path.isfile(clean_json), "Output JSON for clean corpus not created"
        assert os.path.isfile(evil_json), "Output JSON for evil corpus not created"

        with open(clean_json, 'r') as f:
            clean_results = json.load(f)

        with open(evil_json, 'r') as f:
            evil_results = json.load(f)

        clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
        evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]

        clean_failed = []
        for cf in clean_files:
            if not clean_results.get(cf, False):
                clean_failed.append(cf)

        evil_failed = []
        for ef in evil_files:
            # Evil files should be flagged as invalid (False)
            if evil_results.get(ef, True):
                evil_failed.append(ef)

        err_msgs = []
        if clean_failed:
            err_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
        if evil_failed:
            err_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

        assert not err_msgs, " | ".join(err_msgs)