# test_final_state.py
import os
import subprocess
import pytest

def test_detector_script_exists_and_executable():
    detector_path = '/home/user/detector.sh'
    assert os.path.isfile(detector_path), f"Expected detector script at {detector_path} is missing."
    assert os.access(detector_path, os.X_OK), f"Detector script at {detector_path} is not executable."

def test_adversarial_corpus_classification():
    detector_path = '/home/user/detector.sh'
    evil_dir = '/app/corpus/evil/'
    clean_dir = '/app/corpus/clean/'

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    bypassed_evil = []
    for evil_file in evil_files:
        file_path = os.path.join(evil_dir, evil_file)
        result = subprocess.run([detector_path, file_path], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(evil_file)

    modified_clean = []
    for clean_file in clean_files:
        file_path = os.path.join(clean_dir, clean_file)
        result = subprocess.run([detector_path, file_path], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(clean_file)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_gateway_app_modifications():
    gateway_path = '/app/gateway/app.py'
    assert os.path.isfile(gateway_path), f"Gateway app at {gateway_path} is missing."

    with open(gateway_path, 'r') as f:
        content = f.read()

    assert 'detector.sh' in content, "Gateway app does not appear to invoke '/home/user/detector.sh'."
    assert '403' in content, "Gateway app does not appear to return an HTTP 403 status code."
    assert 'MALICIOUS' in content, "Gateway app does not appear to return the 'MALICIOUS' response body."

def test_backend_sandboxing_modifications():
    backend_script_path = '/app/backend/start_backend.sh'
    assert os.path.isfile(backend_script_path), f"Backend start script at {backend_script_path} is missing."

    with open(backend_script_path, 'r') as f:
        content = f.read()

    has_bwrap = 'bwrap' in content
    has_unshare = 'unshare' in content

    assert has_bwrap or has_unshare, "Backend start script does not appear to use 'bwrap' or 'unshare' for sandboxing."