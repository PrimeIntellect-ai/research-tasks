# test_final_state.py

import os
import re
import stat

def test_libmathops_so_exists():
    path = "/home/user/math_migration/libmathops.so"
    assert os.path.isfile(path), f"File {path} does not exist. Makefile was not fixed or run properly."

    # Check if it's an ELF file
    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{path} is not a valid ELF file."

def test_pytest_results_log():
    path = "/home/user/math_migration/pytest_results.log"
    assert os.path.isfile(path), f"File {path} does not exist. Pytest was not run or output not redirected."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for "passed" in the output (usually "2 passed" or similar)
    assert re.search(r"\b\d+ passed\b", content), "pytest_results.log does not indicate successful test passes."

def test_version_log():
    path = "/home/user/math_migration/version.log"
    assert os.path.isfile(path), f"File {path} does not exist. check_version.sh was not run or failed."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.strip() == "VERSION_OK", f"version.log content is incorrect. Expected 'VERSION_OK', got '{content.strip()}'."

def test_check_version_sh():
    path = "/home/user/math_migration/check_version.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check executable permission
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for sort -V or sort -t.
    assert "sort -V" in content or "sort -t" in content, "check_version.sh does not seem to use 'sort -V' or 'sort -t.' for version comparison."