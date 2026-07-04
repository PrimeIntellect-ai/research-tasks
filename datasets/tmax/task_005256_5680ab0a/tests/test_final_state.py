# test_final_state.py

import os
import re

def test_output_file_exists_and_content():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "Processed: 1024.000000"
    assert content == expected_content, f"Output file content is incorrect. Expected '{expected_content}', got '{content}'."

def test_build_sh_includes_math_library():
    build_sh_path = "/home/user/legacy_tool/build.sh"
    assert os.path.isfile(build_sh_path), f"{build_sh_path} does not exist."

    with open(build_sh_path, "r") as f:
        content = f.read()

    assert "-lm" in content, "build.sh does not include the '-lm' flag to correctly link the math library."

def test_run_sh_safely_quotes_argument():
    run_sh_path = "/home/user/legacy_tool/run.sh"
    assert os.path.isfile(run_sh_path), f"{run_sh_path} does not exist."

    with open(run_sh_path, "r") as f:
        content = f.read()

    # Check if the script uses "$1", "$@", "${1}", or "${@}" to safely handle spaces
    pattern = r'"\$1"|"\$@"|"\$\{1\}"|"\$\{@\}"'
    assert re.search(pattern, content), "run.sh does not safely quote the filename argument (e.g., \"$1\")."

def test_recovered_test_file():
    test_case_path = "/home/user/legacy_tool/test case.txt"
    assert os.path.isfile(test_case_path), f"The lost test asset '{test_case_path}' was not recovered."

    with open(test_case_path, "r") as f:
        content = f.read().strip()

    assert content == "1048576", f"The recovered test file '{test_case_path}' does not contain the correct original data."