# test_final_state.py
import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
RUSTY_MATH_DIR = os.path.join(WORKSPACE_DIR, "rusty_math")
CI_PIPELINE_SCRIPT = os.path.join(WORKSPACE_DIR, "ci_pipeline.sh")
DEP_COUNT_FILE = os.path.join(WORKSPACE_DIR, "dep_count.txt")
LIB_RS_FILE = os.path.join(RUSTY_MATH_DIR, "src", "lib.rs")

def test_lib_rs_modified():
    assert os.path.isfile(LIB_RS_FILE), f"{LIB_RS_FILE} is missing."
    with open(LIB_RS_FILE, 'r') as f:
        content = f.read()

    assert "cfg" in content and "wasm32" in content, "lib.rs does not seem to contain #[cfg(...)] attributes for wasm32."

def test_native_build_succeeds():
    result = subprocess.run(
        ["cargo", "build"],
        cwd=RUSTY_MATH_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Native cargo build failed:\n{result.stderr}"

def test_wasm_build_succeeds():
    result = subprocess.run(
        ["cargo", "build", "--target", "wasm32-unknown-unknown"],
        cwd=RUSTY_MATH_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Wasm cargo build failed:\n{result.stderr}"

def test_ci_pipeline_script_executable():
    assert os.path.isfile(CI_PIPELINE_SCRIPT), f"{CI_PIPELINE_SCRIPT} is missing."
    assert os.access(CI_PIPELINE_SCRIPT, os.X_OK), f"{CI_PIPELINE_SCRIPT} is not executable."

def test_dep_count_file_correct():
    assert os.path.isfile(DEP_COUNT_FILE), f"{DEP_COUNT_FILE} is missing."

    with open(DEP_COUNT_FILE, 'r') as f:
        content = f.read().strip()

    try:
        written_count = int(content)
    except ValueError:
        pytest.fail(f"{DEP_COUNT_FILE} does not contain a valid integer. Found: '{content}'")

    # Calculate truth
    tree_result = subprocess.run(
        ["cargo", "tree", "--prefix", "none"],
        cwd=RUSTY_MATH_DIR,
        capture_output=True,
        text=True
    )
    assert tree_result.returncode == 0, "cargo tree command failed."

    deps = set()
    for line in tree_result.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("rusty_math"):
            # cargo tree output lines usually look like: num-traits v0.2.19
            # Just taking the whole line to find unique packages
            deps.add(line)

    expected_count = len(deps)

    assert written_count == expected_count, f"Expected {expected_count} dependencies in {DEP_COUNT_FILE}, but found {written_count}."