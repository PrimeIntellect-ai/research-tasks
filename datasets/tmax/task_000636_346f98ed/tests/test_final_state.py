# test_final_state.py
import os
import sys
import importlib.util

def test_venv_exists():
    assert os.path.isdir('/home/user/venv'), "Virtual environment /home/user/venv does not exist."
    assert os.path.isfile('/home/user/venv/bin/python'), "Python binary not found in venv."

def test_sanitizer_module():
    sanitizer_path = '/home/user/sanitizer.py'
    assert os.path.isfile(sanitizer_path), f"{sanitizer_path} does not exist."

    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        assert False, f"Failed to load sanitizer.py: {e}"

    assert hasattr(sanitizer, 'sanitize_log'), "sanitize_log function not found in sanitizer.py"

    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_failed = []
    for f in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, f)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            if not sanitizer.sanitize_log(content):
                clean_failed.append(f)

    evil_failed = []
    for f in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, f)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            if sanitizer.sanitize_log(content):
                evil_failed.append(f)

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} clean files were incorrectly rejected (modified/flagged): {', '.join(clean_failed[:5])}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} evil files bypassed sanitization (accepted): {', '.join(evil_failed[:5])}")

    assert not error_msgs, " | ".join(error_msgs)

def test_test_files_exist():
    assert os.path.isfile('/home/user/test_sanitizer.py'), "/home/user/test_sanitizer.py does not exist."
    assert os.path.isfile('/home/user/test_report.log'), "/home/user/test_report.log does not exist."