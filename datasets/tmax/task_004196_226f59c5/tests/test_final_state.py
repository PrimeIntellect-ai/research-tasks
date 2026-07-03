# test_final_state.py
import os
import subprocess
import hashlib
import csv

def test_deploy_metadata_csv():
    csv_path = "/home/user/deploy_metadata.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    # Compute expected entry point dynamically
    bin_path = "/home/user/app_v1.bin"
    assert os.path.exists(bin_path), f"File {bin_path} is missing."
    result = subprocess.run(
        ["readelf", "-h", bin_path],
        capture_output=True, text=True, check=True
    )
    entry_point = ""
    for line in result.stdout.splitlines():
        if "Entry point address:" in line:
            entry_point = line.split(":", 1)[1].strip()
            break
    assert entry_point, "Could not extract entry point from ELF binary."

    expected_rows = [
        ["FilePath", "FileType", "Metadata"],
        ["/home/user/app_v1.bin", "ELF", entry_point],
        ["/home/user/local_db.wal", "WAL", "377f0682"],
        ["/home/user/part_a.gcode", "GCODE", "135"]
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"CSV content does not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_deploy_manifest_sha256():
    manifest_path = "/home/user/deploy_manifest.sha256"
    assert os.path.exists(manifest_path), f"File {manifest_path} does not exist."

    files_to_hash = [
        "/home/user/app_v1.bin",
        "/home/user/local_db.wal",
        "/home/user/part_a.gcode"
    ]

    expected_lines = []
    for filepath in files_to_hash:
        assert os.path.exists(filepath), f"File {filepath} is missing."
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        expected_lines.append(f"{file_hash}  {filepath}")

    expected_lines.sort(key=lambda x: x.split("  ")[1])

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Manifest content does not match expected output.\nExpected: {expected_lines}\nActual: {actual_lines}"