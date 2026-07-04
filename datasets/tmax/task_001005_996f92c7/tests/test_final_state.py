# test_final_state.py
import os
import glob
import hashlib
import subprocess
import tempfile
import shutil

def get_expected_results():
    submissions_dir = "/home/user/ci_system/submissions"
    src_dir = "/home/user/ci_system/src"

    meta_files = sorted(glob.glob(os.path.join(submissions_dir, "*.meta")))

    user_timestamps = {}
    expected_results = []

    for meta_file in meta_files:
        base_name = os.path.basename(meta_file)
        sub_id = base_name.replace(".meta", "")
        patch_file = os.path.join(submissions_dir, f"{sub_id}.patch")

        with open(meta_file, "r") as f:
            lines = f.read().splitlines()

        meta_data = {}
        for line in lines:
            if "=" in line:
                k, v = line.split("=", 1)
                meta_data[k.strip()] = v.strip()

        user = meta_data.get("USER")
        timestamp = int(meta_data.get("TIMESTAMP", 0))
        expected_checksum = meta_data.get("CHECKSUM")

        # 1. Rate Limiting
        last_ts = user_timestamps.get(user)
        if last_ts is not None and (timestamp - last_ts) < 60:
            expected_results.append(f"{sub_id} RATE_LIMITED")
            continue

        # Update timestamp for non-rate-limited
        user_timestamps[user] = timestamp

        # 2. Checksum Validation
        with open(patch_file, "rb") as f:
            actual_checksum = hashlib.sha256(f.read()).hexdigest()

        if actual_checksum != expected_checksum:
            expected_results.append(f"{sub_id} CHECKSUM_FAILED")
            continue

        # 3. Patch Processing
        with tempfile.TemporaryDirectory() as tmpdir:
            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
                d = os.path.join(tmpdir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            with open(patch_file, "r") as f:
                patch_proc = subprocess.run(
                    ["patch", "-p1"],
                    stdin=f,
                    cwd=tmpdir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            if patch_proc.returncode != 0:
                expected_results.append(f"{sub_id} PATCH_FAILED")
                continue

            # 4. Testing
            test_proc = subprocess.run(
                ["./math_utils.sh", "test"],
                cwd=tmpdir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if test_proc.returncode != 0:
                expected_results.append(f"{sub_id} TEST_FAILED")
                continue

            # 5. Success
            expected_results.append(f"{sub_id} ACCEPTED")

    return expected_results

def test_results_log():
    results_file = "/home/user/ci_system/results.log"
    assert os.path.isfile(results_file), f"Results file missing: {results_file}"

    with open(results_file, "r") as f:
        actual_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_lines = get_expected_results()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.log, found {len(actual_lines)}"

    for idx, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {idx + 1}: expected '{expected}', got '{actual}'"

def test_script_exists_and_executable():
    script_path = "/home/user/ci_system/process_queue.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script not executable: {script_path}"