# test_final_state.py

import os
import re
import subprocess

PROJECT_DIR = "/home/user/project"
SRC_DIR = "/home/user/project/src"
BUILD_DIR = "/home/user/project/build"
RESULT_FILE = "/home/user/result.txt"

def get_valid_scores():
    """Dynamically compute all valid scores for the CSP."""
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
    valid_scores = set()

    # Node 0 is always color 1
    for c1 in [1, 2, 3]:
        for c2 in [1, 2, 3]:
            for c3 in [1, 2, 3]:
                for c4 in [1, 2, 3]:
                    colors = [1, c1, c2, c3, c4]
                    is_valid = True
                    for u, v in edges:
                        if colors[u] == colors[v]:
                            is_valid = False
                            break
                    if is_valid:
                        # Score = sum(items[i] * (i + 1) * 10)
                        score = sum(colors[i] * (i + 1) * 10 for i in range(5))
                        valid_scores.add(score)

    return valid_scores

def test_cmake_fixed():
    """Test that CMakeLists.txt correctly links the libraries."""
    cmake_path = os.path.join(PROJECT_DIR, "CMakeLists.txt")
    assert os.path.isfile(cmake_path), f"File missing: {cmake_path}"

    with open(cmake_path, "r") as f:
        content = f.read()

    # Check for target_link_libraries
    assert "target_link_libraries" in content and "solver_core" in content and "math_utils" in content, \
        "CMakeLists.txt must use target_link_libraries to link solver_core with math_utils."

def test_c_code_fixed():
    """Test that the C code memory issues are fixed."""
    c_path = os.path.join(SRC_DIR, "solver_core.c")
    assert os.path.isfile(c_path), f"File missing: {c_path}"

    with open(c_path, "r") as f:
        content = f.read()

    # The buffer overflow should be fixed (e.g., i < num_items instead of i <= num_items)
    # We check that the exact buggy string 'i <= num_items' is gone.
    assert "i <= num_items" not in content, "Buffer overflow bug (<= num_items) is still present in solver_core.c."

    # Check for free()
    assert re.search(r"free\s*\(", content), "Memory leak bug is still present: missing free() in solver_core.c."

def test_build_artifacts():
    """Test that the project was built successfully."""
    # The build directory could be structured differently, but we look for the shared libraries
    assert os.path.isdir(BUILD_DIR), f"Build directory missing: {BUILD_DIR}"

    # Find the shared libraries in the build directory
    so_files = []
    for root, dirs, files in os.walk(BUILD_DIR):
        for file in files:
            if file.endswith(".so"):
                so_files.append(file)

    assert any("solver_core" in f for f in so_files), "libsolver_core.so was not found in the build directory."
    assert any("math_utils" in f for f in so_files), "libmath_utils.so was not found in the build directory."

def test_result_file():
    """Test that the result file exists and contains a valid score."""
    assert os.path.isfile(RESULT_FILE), f"Result file missing: {RESULT_FILE}"

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Result file must contain only an integer, got: '{content}'"

    score = int(content)
    valid_scores = get_valid_scores()

    assert score in valid_scores, f"Score {score} is not a valid score for any correct coloring. Valid scores: {valid_scores}"

def test_wrapper_execution():
    """Test that wrapper.py runs without errors."""
    wrapper_path = os.path.join(PROJECT_DIR, "wrapper.py")
    assert os.path.isfile(wrapper_path), f"File missing: {wrapper_path}"

    # Run the wrapper script
    result = subprocess.run(
        ["python3", wrapper_path], 
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"wrapper.py failed to run. Stderr: {result.stderr}"