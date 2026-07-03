# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_file_organization():
    """Check that directories are created and files are moved properly."""
    src_dir = os.path.join(PROJECT_DIR, "src")
    tests_dir = os.path.join(PROJECT_DIR, "tests")
    build_dir = os.path.join(PROJECT_DIR, "build")

    assert os.path.isdir(src_dir), f"{src_dir} directory is missing."
    assert os.path.isdir(tests_dir), f"{tests_dir} directory is missing."
    assert os.path.isdir(build_dir), f"{build_dir} directory is missing."

    # Check new locations
    assert os.path.isfile(os.path.join(src_dir, "processor.c")), "processor.c is not in src/"
    assert os.path.isfile(os.path.join(src_dir, "processor.h")), "processor.h is not in src/"
    assert os.path.isfile(os.path.join(tests_dir, "test_processor.py")), "test_processor.py is not in tests/"

    # Check old locations
    assert not os.path.exists(os.path.join(PROJECT_DIR, "processor.c")), "processor.c was not moved from root."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "processor.h")), "processor.h was not moved from root."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "test_processor.py")), "test_processor.py was not moved from root."

def test_makefile_and_build():
    """Check that Makefile builds the shared library correctly."""
    makefile_path = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(makefile_path), "Makefile is missing."

    # Run make clean to ensure a fresh build
    subprocess.run(["make", "clean"], cwd=PROJECT_DIR, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}"

    # Check if the shared library was created in the correct location
    lib_path = os.path.join(PROJECT_DIR, "build", "libprocessor.so")
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}"

def test_memory_leak_fixed():
    """Check that the C code now contains free()."""
    processor_c_path = os.path.join(PROJECT_DIR, "src", "processor.c")
    assert os.path.isfile(processor_c_path), f"{processor_c_path} not found."

    with open(processor_c_path, "r") as f:
        content = f.read()

    assert "free(" in content, "Memory leak not fixed: free() is missing in processor.c"

def test_python_tests_pass():
    """Run the Python test suite and check if it passes."""
    # Run tests using unittest discover
    result = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Python tests failed:\n{result.stderr}\n{result.stdout}"

def test_valgrind_report():
    """Check that valgrind_report.txt exists and shows no leaks."""
    report_path = os.path.join(PROJECT_DIR, "valgrind_report.txt")
    assert os.path.isfile(report_path), f"Valgrind report not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    # The exact string may vary slightly depending on Valgrind version, but typically it shows:
    # "definitely lost: 0 bytes in 0 blocks"
    assert "definitely lost: 0 bytes in 0 blocks" in content, (
        "Valgrind report does not show 0 bytes definitely lost. "
        f"Report content:\n{content}"
    )