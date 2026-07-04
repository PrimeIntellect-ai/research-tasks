# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/math_util"

def test_build_sh_exists_and_executable():
    build_script = os.path.join(WORKSPACE_DIR, "build.sh")
    assert os.path.isfile(build_script), f"build.sh is missing at {build_script}"
    assert os.access(build_script, os.X_OK), f"build.sh at {build_script} is not executable"

def test_main_go_exists_and_uses_cgo():
    main_go = os.path.join(WORKSPACE_DIR, "main.go")
    assert os.path.isfile(main_go), f"main.go is missing at {main_go}"

    with open(main_go, "r") as f:
        content = f.read()

    assert '"C"' in content, "main.go does not seem to use CGO (missing import \"C\")"

def test_math_runner_exists_and_executable():
    runner = os.path.join(WORKSPACE_DIR, "math_runner")
    assert os.path.isfile(runner), f"math_runner executable is missing at {runner}"
    assert os.access(runner, os.X_OK), f"math_runner at {runner} is not executable"

def test_result_txt_matches_expected():
    result_file = os.path.join(WORKSPACE_DIR, "result.txt")
    expected_file = os.path.join(WORKSPACE_DIR, ".expected")

    assert os.path.isfile(result_file), f"result.txt is missing at {result_file}"
    assert os.path.isfile(expected_file), f"Truth file .expected is missing at {expected_file}"

    with open(result_file, "r") as f:
        result_content = f.read().strip()

    with open(expected_file, "r") as f:
        expected_content = f.read().strip()

    assert result_content == expected_content, f"result.txt content '{result_content}' does not match expected '{expected_content}'"