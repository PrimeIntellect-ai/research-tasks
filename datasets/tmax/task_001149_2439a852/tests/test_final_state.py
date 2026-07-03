# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_deployment_structure():
    current_symlink = "/home/user/opt/edge_sensor/current"
    v2_release_dir = "/home/user/opt/edge_sensor/releases/v2"

    assert os.path.islink(current_symlink), f"{current_symlink} is not a symlink"
    target = os.readlink(current_symlink)
    assert target == v2_release_dir, f"Symlink {current_symlink} points to {target}, expected {v2_release_dir}"

    sensor_filter_path = os.path.join(current_symlink, "sensor_filter")
    libcjson_path = os.path.join(current_symlink, "libcjson.so")

    assert os.path.isfile(sensor_filter_path), f"Missing sensor_filter binary at {sensor_filter_path}"
    assert os.access(sensor_filter_path, os.X_OK), f"sensor_filter at {sensor_filter_path} is not executable"

    assert os.path.isfile(libcjson_path), f"Missing libcjson.so at {libcjson_path}"

def test_backup_logic():
    backup_dummy = "/home/user/opt/edge_sensor/backup/dummy_binary"
    assert os.path.isfile(backup_dummy), f"Backup logic failed: missing {backup_dummy}"

def test_sensor_filter_clean_corpus():
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, "No files found in clean corpus"

    executable = "/home/user/opt/edge_sensor/current/sensor_filter"
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/opt/edge_sensor/current"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([executable, f], env=env, capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_sensor_filter_evil_corpus():
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, "No files found in evil corpus"

    executable = "/home/user/opt/edge_sensor/current/sensor_filter"
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/opt/edge_sensor/current"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([executable, f], env=env, capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"