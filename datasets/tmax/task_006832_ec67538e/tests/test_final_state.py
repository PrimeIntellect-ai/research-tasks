# test_final_state.py

import os
import pytest

def test_plugins_extracted():
    plugins_dir = "/home/user/repo/plugins"
    assert os.path.isdir(plugins_dir), f"Directory {plugins_dir} does not exist. Plugins were not extracted correctly."
    # Check if plugin_beta.so exists inside
    assert os.path.isfile(os.path.join(plugins_dir, "plugin_beta.so")), "plugin_beta.so not found in the extracted plugins directory."

def test_run_tests_script_exists_and_executable():
    script_path = "/home/user/repo/run_tests.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_lib_symlink_correct():
    symlink_path = "/home/user/repo/lib/libprocessor.so"
    assert os.path.islink(symlink_path), f"{symlink_path} does not exist or is not a symlink."

    target = os.readlink(symlink_path)
    # Resolve the absolute path of the target
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))

    expected_target = "/home/user/repo/plugins/plugin_beta.so"
    assert abs_target == expected_target, f"Symlink points to {abs_target}, expected it to resolve to {expected_target}."

def test_output_file_contents():
    output_path = "/home/user/repo/test_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "INIT_ENGINE\nSUCCESS_DATA_PROCESSED_V2"

    assert content == expected_content, f"Output file content is incorrect. Got:\n{content}\nExpected:\n{expected_content}"