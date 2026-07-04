# test_final_state.py

import os
import stat
import pytest

def test_run_operator_script_exists_and_executable():
    script_path = "/home/user/run_operator.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_configs_permissions():
    configs_dir = "/home/user/configs"
    assert os.path.isdir(configs_dir), f"Directory {configs_dir} does not exist."

    dir_stat = os.stat(configs_dir)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o750, f"Permissions for {configs_dir} are not 0750. Got {oct(stat.S_IMODE(dir_stat.st_mode))}."

    for filename in os.listdir(configs_dir):
        filepath = os.path.join(configs_dir, filename)
        if os.path.isfile(filepath):
            file_stat = os.stat(filepath)
            assert stat.S_IMODE(file_stat.st_mode) == 0o640, f"Permissions for {filepath} are not 0640. Got {oct(stat.S_IMODE(file_stat.st_mode))}."

def test_manifests_yaml_exists():
    output_file = "/home/user/output/manifests.yaml"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did the script run successfully?"

def test_manifests_yaml_size():
    output_file = "/home/user/output/manifests.yaml"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    file_size = os.path.getsize(output_file)
    threshold = 2000

    assert file_size <= threshold, f"Metric failed: File size of {output_file} is {file_size} bytes, which is greater than the threshold of {threshold} bytes. The Rust code loop might not be fixed correctly."