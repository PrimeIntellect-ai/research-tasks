# test_final_state.py

import os
import subprocess
import pytest

def test_symlinks_created_correctly():
    build_dir = "/home/user/project/build"
    assert os.path.isdir(build_dir), f"Build directory {build_dir} was not created."

    alpha_link = os.path.join(build_dir, "libAlpha")
    beta_link = os.path.join(build_dir, "libBeta")

    assert os.path.islink(alpha_link), f"{alpha_link} is not a symlink."
    assert os.path.islink(beta_link), f"{beta_link} is not a symlink."

    alpha_target = os.readlink(alpha_link)
    beta_target = os.readlink(beta_link)

    expected_alpha_target = "/home/user/libs/libAlpha-1.2.5"
    expected_beta_target = "/home/user/libs/libBeta-1.1.2"

    assert alpha_target == expected_alpha_target, f"libAlpha symlink points to {alpha_target}, expected {expected_alpha_target}"
    assert beta_target == expected_beta_target, f"libBeta symlink points to {beta_target}, expected {expected_beta_target}"

def test_test_linker_exists_and_uses_hypothesis():
    test_file = "/home/user/project/test_linker.py"
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    with open(test_file, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not appear to import or use 'hypothesis'."
    assert "@given" in content, "The test file does not appear to use the '@given' decorator from hypothesis."

def test_pytest_runs_successfully():
    test_file = "/home/user/project/test_linker.py"
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/user/project"

    result = subprocess.run(
        ["pytest", test_file],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest failed on {test_file}:\n{result.stdout}\n{result.stderr}"