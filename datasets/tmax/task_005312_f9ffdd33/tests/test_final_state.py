# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."

    jpg_files = glob.glob(os.path.join(frames_dir, "*.jpg"))
    assert len(jpg_files) == 10, f"Expected exactly 10 frames extracted, found {len(jpg_files)}: {jpg_files}"

def test_sanitiser_script_clean_corpus():
    sanitiser_path = "/home/user/sanitiser.py"
    clean_dir = "/home/user/metadata/clean/"

    assert os.path.isfile(sanitiser_path), f"Sanitiser script not found at {sanitiser_path}"

    result = subprocess.run(["python3", sanitiser_path, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Sanitiser script failed on clean corpus with error:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]

    failed_clean = []
    for f in clean_files:
        # We expect the output to contain the filename and 'PASS'
        # e.g., "clean1.json PASS"
        found_pass = any(f in line and "PASS" in line for line in output_lines)
        if not found_pass:
            failed_clean.append(f)

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected (expected PASS). Offending files: {failed_clean}"

def test_sanitiser_script_evil_corpus():
    sanitiser_path = "/home/user/sanitiser.py"
    evil_dir = "/home/user/metadata/evil/"

    assert os.path.isfile(sanitiser_path), f"Sanitiser script not found at {sanitiser_path}"

    result = subprocess.run(["python3", sanitiser_path, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Sanitiser script failed on evil corpus with error:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    bypassed_evil = []
    for f in evil_files:
        # We expect the output to contain the filename and 'FAIL'
        found_fail = any(f in line and "FAIL" in line for line in output_lines)
        if not found_fail:
            bypassed_evil.append(f)

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed (expected FAIL). Offending files: {bypassed_evil}"

def test_ci_pipeline_and_benchmark():
    ci_script = "/home/user/ci_pipeline.sh"
    benchmark_log = "/home/user/benchmark.log"

    assert os.path.isfile(ci_script), f"CI pipeline script not found at {ci_script}"
    assert os.access(ci_script, os.X_OK), f"CI pipeline script {ci_script} is not executable"

    assert os.path.isfile(benchmark_log), f"Benchmark log not found at {benchmark_log}"
    assert os.path.getsize(benchmark_log) > 0, f"Benchmark log {benchmark_log} is empty"