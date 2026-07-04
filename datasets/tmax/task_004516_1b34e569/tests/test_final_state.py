# test_final_state.py

import os

SUCCESS_FILE = "/home/user/success.txt"
EXPECTED_CONTENT = "BUILD_PASS_774"

def test_success_file_exists_and_correct():
    assert os.path.exists(SUCCESS_FILE), (
        f"The success file {SUCCESS_FILE} does not exist. "
        "Make sure you fixed build.py, provided the correct CI_TOKEN, and ran the build script."
    )

    with open(SUCCESS_FILE, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_CONTENT, (
        f"The content of {SUCCESS_FILE} is incorrect. "
        f"Expected '{EXPECTED_CONTENT}', but got '{content}'."
    )

def test_build_script_fixed():
    # Also verify that build.py was fixed to use "test/" instead of "tests/"
    # or at least that it no longer contains the buggy path if it was modified.
    build_script = "/home/user/project/build.py"
    if os.path.exists(build_script):
        with open(build_script, "r") as f:
            content = f.read()
        # The script should point to the existing test directory.
        assert 'TEST_DIR = "tests/"' not in content, (
            "The build script still contains the incorrect TEST_DIR path 'tests/'."
        )