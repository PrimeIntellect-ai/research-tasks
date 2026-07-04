# test_final_state.py

import os
import json
import pytest

def test_extraction_log():
    log_path = "/home/user/extraction.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_line = "MALICIOUS: ../../../escape.sh"
    assert expected_line in content, f"Expected '{expected_line}' in {log_path}, but got: {content}"

    lines = [line for line in content.split('\n') if line.strip()]
    assert len(lines) == 1, f"Expected exactly 1 malicious file logged, but found {len(lines)}."

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {report_path} as JSON: {e}")

    assert "extracted_files" in report, "Missing 'extracted_files' in report.json"
    extracted_files = set(report["extracted_files"])
    assert "bin/app.elf" in extracted_files, "bin/app.elf missing from extracted_files"
    assert "metadata.txt" in extracted_files, "metadata.txt missing from extracted_files"
    assert len(extracted_files) == 2, f"Expected 2 extracted files in report, got {len(extracted_files)}"

    assert report.get("malicious_files_prevented") == 1, "Expected malicious_files_prevented to be 1"

    assert "elf_entry_points" in report, "Missing 'elf_entry_points' in report.json"
    assert report["elf_entry_points"].get("bin/app.elf") == "0x401000", "Incorrect or missing ELF entry point for bin/app.elf"

    expected_metadata = "Version: 1.2.4\nAuthor: SecOps"
    assert report.get("metadata_text") == expected_metadata, "Incorrect metadata_text in report.json"

def test_extracted_files_exist():
    app_elf_path = "/home/user/extracted/bin/app.elf"
    metadata_path = "/home/user/extracted/metadata.txt"

    assert os.path.isfile(app_elf_path), f"Extracted file {app_elf_path} does not exist."
    assert os.path.isfile(metadata_path), f"Extracted file {metadata_path} does not exist."

    # Check that the malicious file was NOT extracted relative to the bundle or extraction dir
    malicious_path_1 = "/home/user/escape.sh"
    malicious_path_2 = "/escape.sh"

    assert not os.path.exists(malicious_path_1), f"Malicious file was extracted to {malicious_path_1}"
    assert not os.path.exists(malicious_path_2), f"Malicious file was extracted to {malicious_path_2}"