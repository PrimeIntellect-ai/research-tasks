# test_final_state.py

import os
import tarfile
import tempfile
import subprocess
import pytest

ARCHIVES_DIR = "/home/user/archives"
SUMMARY_FILE = "/home/user/docs_summary.txt"

VALID_ARCHIVES = [
    "arch_alpha.tar.gz",
    "arch_beta.tar.gz",
    "arch_gamma.tar.gz"
]

def get_entry_point(bin_path):
    result = subprocess.run(["readelf", "-h", bin_path], capture_output=True, text=True, check=True)
    for line in result.stdout.splitlines():
        if "Entry point address:" in line:
            return line.split(":")[1].strip()
    return ""

def test_docs_summary_exists():
    assert os.path.isfile(SUMMARY_FILE), f"The summary file {SUMMARY_FILE} does not exist."

def test_docs_summary_content():
    assert os.path.isfile(SUMMARY_FILE), f"The summary file {SUMMARY_FILE} does not exist."

    expected_lines = []
    for arch in VALID_ARCHIVES:
        arch_path = os.path.join(ARCHIVES_DIR, arch)
        assert os.path.isfile(arch_path), f"Expected archive {arch_path} is missing."

        with tarfile.open(arch_path, "r:gz") as tar:
            # Get first line of readme.md
            readme_file = tar.extractfile("readme.md")
            assert readme_file is not None, f"readme.md missing in {arch}"
            first_line = readme_file.readline().decode("utf-8").strip()

            # Extract app.bin to a temp directory to run readelf
            with tempfile.TemporaryDirectory() as tmpdir:
                tar.extract("app.bin", path=tmpdir)
                bin_path = os.path.join(tmpdir, "app.bin")
                entry_point = get_entry_point(bin_path)

            expected_lines.append(f"{arch} | {first_line} | {entry_point}")

    expected_lines.sort()

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {SUMMARY_FILE}, found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} in {SUMMARY_FILE} does not match expected output.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )