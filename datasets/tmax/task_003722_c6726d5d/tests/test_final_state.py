# test_final_state.py

import os
import re

def test_tmp_files_cleanup():
    small_tmp = '/home/user/project/small.tmp'
    large1_tmp = '/home/user/project/large1.tmp'
    large2_tmp = '/home/user/project/sub/large2.tmp'

    assert os.path.isfile(small_tmp), f"FAIL: {small_tmp} should not have been deleted (it is <= 10KB)."
    assert not os.path.exists(large1_tmp), f"FAIL: {large1_tmp} was not deleted (it is > 10KB)."
    assert not os.path.exists(large2_tmp), f"FAIL: {large2_tmp} was not deleted (it is > 10KB)."

def test_config_updated():
    config_path = '/home/user/project/config.ini'
    assert os.path.isfile(config_path), f"FAIL: {config_path} is missing."

    with open(config_path, 'r') as f:
        content = f.read()

    assert 'LOG_LEVEL=INFO' in content, "FAIL: config.ini does not contain LOG_LEVEL=INFO."
    assert 'LOG_LEVEL=DEBUG' not in content, "FAIL: config.ini still contains LOG_LEVEL=DEBUG."

def test_errors_found_log():
    log_path = '/home/user/project/errors_found.log'
    assert os.path.isfile(log_path), f"FAIL: {log_path} was not created."

    with open(log_path, 'r') as f:
        content = f.read()

    error_count = len(re.findall(r'^\[ERROR\]', content, re.MULTILINE))
    info_count = len(re.findall(r'^\[INFO\]', content, re.MULTILINE))

    assert error_count == 3, f"FAIL: Expected exactly 3 [ERROR] records, found {error_count}."
    assert info_count == 0, f"FAIL: Expected 0 [INFO] records, found {info_count}."
    assert "Traceback" in content, "FAIL: Multi-line traceback content is missing from the parsed errors."