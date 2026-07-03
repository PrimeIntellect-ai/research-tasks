# test_final_state.py

import os
import tarfile
import pytest

def test_ci_tool_script_exists_and_executable():
    script_path = "/home/user/ci_tool.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_main_rs_patched():
    main_rs_path = "/home/user/project/src/main.rs"
    assert os.path.isfile(main_rs_path), f"The file {main_rs_path} does not exist."
    with open(main_rs_path, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 3, "main.rs does not have enough lines."
    # The patch should be on line 3 (index 2)
    assert "let s2 = s1.clone();" in lines[2], "Line 3 of main.rs was not correctly patched with .clone();"

def test_ci_report_log():
    report_path = "/home/user/project/ci_report.log"
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "[x86] Status: FAILED_BUT_FIXED",
        "[arm] Status: FAILED_BUT_FIXED",
        "Patched line: 3"
    ]

    for expected_line in expected_lines:
        assert expected_line in content, f"Expected '{expected_line}' in ci_report.log, but it was missing or incorrect."

def test_tarball_exists_and_valid():
    tarball_path = "/home/user/project/src_archive.tar.gz"
    assert os.path.isfile(tarball_path), f"The tarball {tarball_path} does not exist."

    assert tarfile.is_tarfile(tarball_path), f"The file {tarball_path} is not a valid tar archive."

    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()
        # The tarball should contain main.rs (either as src/main.rs or main.rs depending on how it was tarred)
        assert any(name.endswith("main.rs") for name in names), "The tarball does not contain main.rs."