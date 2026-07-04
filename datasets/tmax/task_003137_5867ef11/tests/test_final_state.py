# test_final_state.py
import os

def test_audit_log_contents():
    log_path = "/home/user/artifact_audit.log"
    assert os.path.isfile(log_path), f"Audit log file is missing at {log_path}."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "[REJECTED] broken_data.zip: Corrupted",
        "[REJECTED] malicious_payload.zip: Path Traversal",
        "[REJECTED] sneaky_lib.tar.gz: Path Traversal"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, (
        f"Audit log contents do not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_quarantine_directory_contents():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Quarantine directory missing at {quarantine_dir}."

    expected_files = {"broken_data.zip", "malicious_payload.zip", "sneaky_lib.tar.gz"}
    actual_files = set(os.listdir(quarantine_dir))

    assert actual_files == expected_files, (
        f"Quarantine directory does not contain exactly the expected files.\n"
        f"Expected: {expected_files}\n"
        f"Actual: {actual_files}"
    )

def test_curated_artifacts_extracted():
    curated_dir = "/home/user/curated_artifacts"
    assert os.path.isdir(curated_dir), f"Curated artifacts directory missing at {curated_dir}."

    safe_app_main = os.path.join(curated_dir, "safe_app", "app", "main.py")
    safe_app_data = os.path.join(curated_dir, "safe_app", "app", "data.bin")
    safe_lib_util = os.path.join(curated_dir, "safe_lib", "lib", "util.py")

    assert os.path.isfile(safe_app_main), f"Expected extracted file is missing: {safe_app_main}"
    assert os.path.isfile(safe_app_data), f"Expected extracted file is missing: {safe_app_data}"
    assert os.path.isfile(safe_lib_util), f"Expected extracted file is missing: {safe_lib_util}"

def test_incoming_directory_is_empty():
    incoming_dir = "/home/user/incoming_artifacts"
    assert os.path.isdir(incoming_dir), f"Incoming artifacts directory missing at {incoming_dir}."

    actual_files = os.listdir(incoming_dir)
    assert len(actual_files) == 0, f"Incoming directory should be empty, but contains: {actual_files}"