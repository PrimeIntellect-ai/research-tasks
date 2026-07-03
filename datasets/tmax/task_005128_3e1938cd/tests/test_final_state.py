# test_final_state.py
import os
import subprocess
import shutil
import pytest

def test_vendored_package_fixed():
    file_path = "/app/vendored/fsmeta-utils/fsmeta/validators.py"
    assert os.path.isfile(file_path), f"Validators file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    buggy_line = "def validate_quota(size_bytes) return size_bytes > 0"
    assert buggy_line not in content, f"The deliberate syntax error was not fixed in {file_path}."

    # Verify the package is importable
    try:
        subprocess.run(
            ["python3", "-c", "from fsmeta.validators import validate_quota"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import fsmeta.validators. Did you install the package? Error: {e.stderr}")

def test_script_exists():
    script_path = "/home/user/validate_mounts.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def run_script(corpus_dir):
    script_path = "/home/user/validate_mounts.py"
    env = os.environ.copy()
    env["TZ"] = "Etc/UTC"

    result = subprocess.run(
        ["python3", script_path, corpus_dir],
        capture_output=True,
        text=True,
        env=env
    )
    return result

def setup_test_env():
    accepted_dir = "/home/user/accepted_mounts"
    rejected_log = "/home/user/rejected.log"

    if os.path.exists(accepted_dir):
        shutil.rmtree(accepted_dir)
    if os.path.exists(rejected_log):
        os.remove(rejected_log)

def get_rejected_files():
    rejected_log = "/home/user/rejected.log"
    if not os.path.exists(rejected_log):
        return set()
    with open(rejected_log, "r") as f:
        return set(line.strip() for line in f if line.strip())

def get_accepted_files():
    accepted_dir = "/home/user/accepted_mounts"
    if not os.path.exists(accepted_dir):
        return set()
    return set(os.listdir(accepted_dir))

def test_clean_corpus():
    setup_test_env()
    corpus_dir = "/app/tests/corpora/clean"
    assert os.path.isdir(corpus_dir), f"Clean corpus directory {corpus_dir} missing."

    clean_files = set(f for f in os.listdir(corpus_dir) if f.endswith(".json"))

    res = run_script(corpus_dir)
    assert res.returncode == 0, f"Script failed on clean corpus:\n{res.stderr}"

    accepted = get_accepted_files()
    rejected = get_rejected_files()

    missing_accepted = clean_files - accepted
    assert not missing_accepted, f"{len(missing_accepted)} of {len(clean_files)} clean files were NOT accepted: {missing_accepted}"

    wrongly_rejected = clean_files.intersection(rejected)
    assert not wrongly_rejected, f"{len(wrongly_rejected)} clean files were wrongly rejected: {wrongly_rejected}"

def test_evil_corpus():
    setup_test_env()
    corpus_dir = "/app/tests/corpora/evil"
    assert os.path.isdir(corpus_dir), f"Evil corpus directory {corpus_dir} missing."

    evil_files = set(f for f in os.listdir(corpus_dir) if f.endswith(".json"))

    res = run_script(corpus_dir)
    assert res.returncode == 0, f"Script failed on evil corpus:\n{res.stderr}"

    accepted = get_accepted_files()
    rejected = get_rejected_files()

    wrongly_accepted = evil_files.intersection(accepted)
    assert not wrongly_accepted, f"{len(wrongly_accepted)} of {len(evil_files)} evil files bypassed sanitization and were accepted: {wrongly_accepted}"

    missing_rejected = evil_files - rejected
    assert not missing_rejected, f"{len(missing_rejected)} evil files were NOT logged in rejected.log: {missing_rejected}"