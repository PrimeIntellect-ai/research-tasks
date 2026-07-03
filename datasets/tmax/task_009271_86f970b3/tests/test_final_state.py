# test_final_state.py

import os
import subprocess
import re
import pytest

INCOMING_DIR = "/home/user/incoming_artifacts"
CURATED_DIR = "/home/user/curated_repo"
REPORT_PATH = "/home/user/artifact_report.txt"
BACKUP_INC_TAR = "/home/user/backups/inc.tar"

def get_elf_info(filepath):
    """Run readelf -h and extract Machine and Type."""
    try:
        output = subprocess.check_output(["readelf", "-h", filepath], stderr=subprocess.DEVNULL, text=True)
    except subprocess.CalledProcessError:
        return None, None

    machine = None
    elf_type = None

    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Type:"):
            val = line.split(":", 1)[1].strip()
            if "EXEC" in val:
                elf_type = "executable"
            elif "DYN" in val:
                elf_type = "shared"
        elif line.startswith("Machine:"):
            val = line.split(":", 1)[1].strip()
            # Replace spaces with underscores, remove hyphens
            machine = val.replace(" ", "_").replace("-", "")

    return machine, elf_type

def get_expected_state():
    expected_files = {}
    counts = {}

    if not os.path.isdir(INCOMING_DIR):
        return expected_files, counts

    for filename in os.listdir(INCOMING_DIR):
        filepath = os.path.join(INCOMING_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        machine, elf_type = get_elf_info(filepath)
        if machine and elf_type:
            expected_files[filename] = {
                "machine": machine,
                "type": elf_type,
                "src_path": filepath
            }

            if machine not in counts:
                counts[machine] = {"executable": 0, "shared": 0}
            counts[machine][elf_type] += 1

    return expected_files, counts

def test_curated_repo_structure_and_hardlinks():
    expected_files, _ = get_expected_state()
    assert expected_files, "No valid ELF files found in incoming_artifacts to test against."

    for filename, info in expected_files.items():
        expected_dir = os.path.join(CURATED_DIR, info["machine"], info["type"])
        expected_path = os.path.join(expected_dir, filename)

        assert os.path.isdir(expected_dir), f"Directory {expected_dir} does not exist."
        assert os.path.isfile(expected_path), f"File {expected_path} does not exist."

        src_stat = os.stat(info["src_path"])
        dst_stat = os.stat(expected_path)

        assert src_stat.st_ino == dst_stat.st_ino, f"{expected_path} is not a hard link to {info['src_path']}."
        assert src_stat.st_dev == dst_stat.st_dev, f"{expected_path} is on a different device."

def test_artifact_report():
    _, counts = get_expected_state()
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    expected_lines = []
    for machine in sorted(counts.keys()):
        exec_count = counts[machine]["executable"]
        shared_count = counts[machine]["shared"]
        expected_lines.append(f"{machine} -> Executables: {exec_count}, Shared: {shared_count}")

    with open(REPORT_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Report content mismatch. Expected: {expected_lines}, Got: {actual_lines}"

def test_incremental_backup():
    assert os.path.isfile(BACKUP_INC_TAR), f"Incremental backup {BACKUP_INC_TAR} is missing."

    try:
        output = subprocess.check_output(["tar", "-tf", BACKUP_INC_TAR], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read incremental tar archive: {e.output}")

    # Check if curated_repo is in the tar archive
    assert any("curated_repo" in line for line in output.splitlines()), "curated_repo not found in the incremental backup."