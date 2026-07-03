# test_final_state.py
import os
import subprocess
import pytest

def run_profiler(h5_path, wav_path):
    script_path = "/home/user/profiler.py"
    if not os.path.isfile(script_path):
        pytest.fail(f"Script missing: {script_path}")

    cmd = ["python3", script_path, h5_path, wav_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Process exited with {e.returncode}. Stderr: {e.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout"

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"
    wav_path = "/app/reference_profile.wav"

    if not os.path.isdir(clean_dir):
        pytest.fail(f"Clean corpus directory missing at {clean_dir}")
    if not os.path.isdir(evil_dir):
        pytest.fail(f"Evil corpus directory missing at {evil_dir}")

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.h5')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.h5')]

    if not clean_files:
        pytest.fail("No HDF5 files found in clean corpus.")
    if not evil_files:
        pytest.fail("No HDF5 files found in evil corpus.")

    failed_clean = []
    failed_evil = []

    for fpath in clean_files:
        output = run_profiler(fpath, wav_path)
        if output != "CLEAN":
            failed_clean.append((os.path.basename(fpath), output))

    for fpath in evil_files:
        output = run_profiler(fpath, wav_path)
        if output != "EVIL":
            failed_evil.append((os.path.basename(fpath), output))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean files misclassified (expected CLEAN). Offending: {failed_clean}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (expected EVIL). Offending: {failed_evil}")

    if errors:
        pytest.fail(" | ".join(errors))