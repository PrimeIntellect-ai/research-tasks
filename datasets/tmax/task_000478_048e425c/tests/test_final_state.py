# test_final_state.py

import os
import glob
import subprocess
import pytest

def get_sanitiser_cmd():
    sanitisers = glob.glob('/home/user/sanitiser.*')
    if not sanitisers:
        pytest.fail("No sanitiser script found at /home/user/sanitiser.*")

    script = sanitisers[0]
    ext = os.path.splitext(script)[1]

    if ext == '.py':
        return ['python3', script]
    elif ext == '.rb':
        return ['ruby', script]
    elif ext == '.js':
        return ['node', script]
    elif ext == '.sh':
        return ['bash', script]
    else:
        # Try to run it directly if it's executable
        if os.access(script, os.X_OK):
            return [script]
        pytest.fail(f"Unknown extension for sanitiser script: {script}")

def test_shortest_path_output():
    """Test that the shortest path is correctly computed and saved."""
    path_file = "/home/user/shortest_path.txt"
    assert os.path.isfile(path_file), f"Missing shortest path output file: {path_file}"

    with open(path_file, 'r') as f:
        content = f.read().strip()

    expected = "ALPHA_01,BETA_04,GAMMA_02,NODE_OMEGA"
    assert content == expected, f"Incorrect shortest path. Expected '{expected}', got '{content}'"

def test_sanitiser_adversarial_corpus():
    """Test the sanitiser script against the clean and evil corpora."""
    cmd_base = get_sanitiser_cmd()

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(cmd_base + [cf], capture_output=True, text=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(cmd_base + [ef], capture_output=True, text=True)
        # It must exit with code 1 OR filter out the malicious nodes (exit 0 but output doesn't contain malicious loop)
        if result.returncode == 0:
            if '__malicious_loop__' in result.stdout:
                evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))