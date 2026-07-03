# test_final_state.py

import os
import re

def test_cargo_toml_fixed():
    cargo_path = "/home/user/pr_review/rust_interner/Cargo.toml"
    assert os.path.isfile(cargo_path), f"File {cargo_path} is missing."
    with open(cargo_path, 'r') as f:
        content = f.read()
        assert "crate-type" in content and "staticlib" in content, "Cargo.toml must specify crate-type = [\"staticlib\"]"

def test_valgrind_report_exists():
    report_path = "/home/user/valgrind_report.txt"
    assert os.path.isfile(report_path), f"Valgrind report {report_path} is missing."

def test_valgrind_report_no_leaks():
    report_path = "/home/user/valgrind_report.txt"
    assert os.path.isfile(report_path), f"Valgrind report {report_path} is missing."
    with open(report_path, 'r') as f:
        content = f.read()

        # Check for successful test run output
        assert "Tests passed." in content, "The test executable did not print 'Tests passed.' Check if it ran successfully."

        # Check for valgrind leak info
        no_leaks_possible = "All heap blocks were freed -- no leaks are possible" in content
        definitely_lost_zero = re.search(r"definitely lost:\s+0 bytes in 0 blocks", content) is not None

        assert no_leaks_possible or definitely_lost_zero, "Valgrind report does not show 0 bytes definitely lost. Memory leak is not fully fixed."

def test_executable_exists():
    exe_path = "/home/user/pr_review/test_runner"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you run make?"