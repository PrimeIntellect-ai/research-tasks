# test_final_state.py
import os
import subprocess
import glob
import pytest

def find_validator():
    # Try common names/extensions
    for ext in ['.py', '.sh', '.js', '']:
        path = f"/home/user/validator{ext}"
        if os.path.isfile(path):
            return path
    # Fallback to glob
    matches = glob.glob("/home/user/validator*")
    if matches:
        return matches[0]
    return None

def run_validator(script_path, target_file):
    if script_path.endswith('.py'):
        cmd = ["python3", script_path, target_file]
    elif script_path.endswith('.js'):
        cmd = ["node", script_path, target_file]
    elif script_path.endswith('.sh') or os.access(script_path, os.X_OK):
        cmd = [script_path, target_file]
    else:
        cmd = ["python3", script_path, target_file] # fallback

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def test_validator_exists():
    script_path = find_validator()
    assert script_path is not None, "Could not find validator script in /home/user/"

def test_clean_corpus():
    script_path = find_validator()
    if not script_path:
        pytest.fail("Validator script missing.")

    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"{clean_dir} missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "Clean corpus is empty."

    failed_files = []
    for f in clean_files:
        output = run_validator(script_path, f)
        if output != "ACCEPT":
            failed_files.append((os.path.basename(f), output))

    if failed_files:
        details = ", ".join([f"{name} (got {out})" for name, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected or errored: {details}")

def test_evil_corpus():
    script_path = find_validator()
    if not script_path:
        pytest.fail("Validator script missing.")

    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"{evil_dir} missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "Evil corpus is empty."

    failed_files = []
    for f in evil_files:
        output = run_validator(script_path, f)
        if output != "REJECT":
            failed_files.append((os.path.basename(f), output))

    if failed_files:
        details = ", ".join([f"{name} (got {out})" for name, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed validation: {details}")