# test_final_state.py

import os
import subprocess
import tarfile

def test_elf_report_exists_and_content_correct():
    """Verify that elf_report.txt is created and contains the correct formatted output."""
    report_path = "/home/user/elf_report.txt"
    assert os.path.isfile(report_path), f"The ELF report is missing: {report_path}"

    # Determine the expected architecture string dynamically
    try:
        out = subprocess.check_output(["readelf", "-h", "/bin/ls"], universal_newlines=True)
        arch = ""
        for line in out.splitlines():
            if "Machine:" in line:
                arch = line.split("Machine:")[1].strip()
                break
    except Exception as e:
        arch = "Advanced Micro Devices X86-64" # Fallback if readelf fails, though it shouldn't

    expected_lines = [
        f"bin/tool_cat - {arch}",
        f"bin/tool_ls - {arch}",
        f"nested_dir/inner_bin/tool_echo - {arch}"
    ]

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # The task requires the report to be sorted alphabetically by file path
    assert actual_lines == sorted(expected_lines), (
        f"elf_report.txt contents do not match the expected output or are not sorted correctly.\n"
        f"Expected: {sorted(expected_lines)}\n"
        f"Actual: {actual_lines}"
    )

def test_filtered_backup_archive():
    """Verify that filtered_backup.tar.gz exists and contains only the correct files."""
    backup_path = "/home/user/filtered_backup.tar.gz"
    assert os.path.isfile(backup_path), f"The filtered backup archive is missing: {backup_path}"

    with tarfile.open(backup_path, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
        file_paths = [m.name for m in members]

        # Clean paths to remove potential leading './'
        cleaned_paths = {p[2:] if p.startswith("./") else p for p in file_paths}

        expected_files = {
            "bin/tool_cat",
            "bin/tool_ls",
            "nested_dir/inner_bin/tool_echo",
            "shape1.gcode",
            "nested_dir/shape2.gcode"
        }

        assert len(cleaned_paths) == 5, f"Incorrect number of files in {backup_path}. Expected 5, found {len(cleaned_paths)}."

        missing_files = expected_files - cleaned_paths
        assert not missing_files, f"Missing expected files in archive: {missing_files}"

        extra_files = cleaned_paths - expected_files
        assert not extra_files, f"Archive contains unauthorized files: {extra_files}"

        for p in cleaned_paths:
            assert not p.endswith(".txt"), f"Archive contains unauthorized .txt file: {p}"
            assert not p.endswith(".log"), f"Archive contains unauthorized .log file: {p}"