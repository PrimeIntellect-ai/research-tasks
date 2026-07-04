# test_final_state.py

import os
import json
import subprocess
import pytest

def test_perturbation_fixed():
    elffile_path = "/app/vendored/pyelftools-0.31/elftools/elf/elffile.py"
    assert os.path.isfile(elffile_path), f"File {elffile_path} does not exist."

    with open(elffile_path, "rb") as f:
        content = f.read()

    assert b"\\x7fFLE" not in content, "The perturbation (b'\\x7fFLE') is still present in elffile.py."
    assert b"\\x7fELF" in content, "The correct ELF magic (b'\\x7fELF') was not restored in elffile.py."

def run_script_and_get_report(target_dir):
    script_path = "/home/user/elf_filter.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    report_path = "/home/user/elf_report.json"
    if os.path.exists(report_path):
        os.remove(report_path)

    result = subprocess.run(
        ["python3", script_path, target_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on {target_dir}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.isfile(report_path), f"Script did not produce {report_path} after running on {target_dir}."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    return report

def test_clean_corpus():
    clean_dir = "/home/user/elf_storage/clean"
    report = run_script_and_get_report(clean_dir)

    expected_files = ["ls_bin", "cat_bin", "echo_bin"]
    failed_files = []

    for fname in expected_files:
        abs_path = os.path.join(clean_dir, fname)
        if abs_path not in report:
            failed_files.append(f"{fname} (missing from report)")
        elif report[abs_path] != "preserve":
            failed_files.append(f"{fname} (mapped to '{report[abs_path]}', expected 'preserve')")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(expected_files)} clean files modified/rejected: " + ", ".join(failed_files))

def test_evil_corpus():
    evil_dir = "/home/user/elf_storage/evil"
    report = run_script_and_get_report(evil_dir)

    expected_files = ["corrupted_magic.elf", "bad_shoff.elf", "bloated.elf"]
    failed_files = []

    for fname in expected_files:
        abs_path = os.path.join(evil_dir, fname)
        if abs_path not in report:
            failed_files.append(f"{fname} (missing from report)")
        elif report[abs_path] != "delete":
            failed_files.append(f"{fname} (mapped to '{report[abs_path]}', expected 'delete')")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(expected_files)} evil files bypassed: " + ", ".join(failed_files))