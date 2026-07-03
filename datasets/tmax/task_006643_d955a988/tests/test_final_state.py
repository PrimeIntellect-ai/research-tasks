# test_final_state.py

import os
import re
import subprocess

def test_poly_math_c_exists():
    path = "/home/user/service_repo/poly_math.c"
    assert os.path.isfile(path), f"{path} does not exist. The file was not properly recovered."

def test_math_service_executable():
    path = "/home/user/service_repo/math_service"
    assert os.path.isfile(path), f"{path} does not exist. The service was not compiled."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_results_txt():
    path = "/home/user/service_repo/results.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you run the compiled executable?"
    with open(path, "r") as f:
        content = f.read().strip()

    # The unmodified math logic produces 750.00
    assert "Final Sum: 750.00" in content, f"Unexpected content in results.txt: '{content}'. The math logic might have been altered."

def test_leak_report():
    path = "/home/user/leak_report.txt"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # The original leak is on line 9
    match = re.search(r"(?i)line[\s:]*9\b", content)
    assert match is not None, f"Leak report does not contain the correct line number (9). Content found: '{content.strip()}'"

def test_valgrind_no_leaks():
    executable_path = "/home/user/service_repo/math_service"
    assert os.path.exists(executable_path), "Cannot run valgrind because math_service is missing."

    result = subprocess.run(
        ["valgrind", "--leak-check=full", "./math_service"],
        cwd="/home/user/service_repo",
        capture_output=True,
        text=True
    )

    # Valgrind outputs its memory check report to stderr
    output = result.stderr
    assert "definitely lost: 0 bytes in 0 blocks" in output, "Memory leak detected by valgrind. The leak in poly_math.c was not fully resolved."