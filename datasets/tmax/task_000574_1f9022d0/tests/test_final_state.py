# test_final_state.py
import os

def test_system_master_utf8():
    path = "/home/user/config_archive/system_master_utf8.ini"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "rb") as f:
        content = f.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        assert False, f"File {path} is not valid UTF-8."

    assert "[MODULE_ALPHA]" in text, f"File {path} missing expected content."
    assert "café" in text, f"File {path} missing expected UTF-8 characters."

def test_split_config_executable():
    c_file = "/home/user/split_config.c"
    bin_file = "/home/user/split_config"

    assert os.path.isfile(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(bin_file), f"Executable {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"File {bin_file} is not executable."

def test_active_configs_symlinks():
    active_dir = "/home/user/active_configs"
    assert os.path.isdir(active_dir), f"Directory {active_dir} does not exist."

    expected_symlinks = ["module_00.ini", "module_02.ini", "module_04.ini"]
    unexpected_symlinks = ["module_01.ini", "module_03.ini"]

    for sym in expected_symlinks:
        sym_path = os.path.join(active_dir, sym)
        assert os.path.islink(sym_path), f"Expected symlink {sym_path} does not exist or is not a symlink."
        target = os.readlink(sym_path)
        assert os.path.isabs(target), f"Symlink {sym_path} does not point to an absolute path."
        assert target == f"/home/user/config_archive/{sym}", f"Symlink {sym_path} points to incorrect target {target}."

    for sym in unexpected_symlinks:
        sym_path = os.path.join(active_dir, sym)
        assert not os.path.exists(sym_path), f"Unexpected symlink {sym_path} should not exist."

def test_active_master_content():
    path = "/home/user/active_master.ini"
    assert os.path.isfile(path), f"File {path} does not exist."

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        assert False, f"File {path} is not valid UTF-8."

    expected_content = """[MODULE_ALPHA]
description=Legacy cache system
status=active
path=/var/cache/app
param1=café
[MODULE_GAMMA]
description=Network bridge
status=active
bridge_name=br0
note=façade
[MODULE_EPSILON]
description=Metrics aggregator
status=active
interval=60
tag=piñata
"""
    assert content.strip() == expected_content.strip(), f"Content of {path} does not match the expected active modules."