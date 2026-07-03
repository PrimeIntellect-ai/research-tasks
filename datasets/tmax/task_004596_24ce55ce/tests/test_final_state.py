# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import pytest

def test_systemd_dependency():
    path = "/home/user/.config/systemd/user/profile-backend.service"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "After=stub-net.service" in content, f"Missing 'After=stub-net.service' in {path}."

def test_nginx_configuration():
    path = "/home/user/deploy/nginx.conf"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://localhost:8084;" in content or "proxy_pass http://127.0.0.1:8084;" in content, \
        f"Nginx configuration {path} does not contain the correct proxy_pass directive for port 8084."

def test_timer_active():
    try:
        # Check if timer is active
        # The user is 'user', so we might need to specify XDG_RUNTIME_DIR or run as user
        # But tests are usually run as the user or root. We'll use systemctl --user
        env = os.environ.copy()
        env["XDG_RUNTIME_DIR"] = "/run/user/1000"
        result = subprocess.run(["systemctl", "--user", "is-active", "profile-sync.timer"], 
                                capture_output=True, text=True, env=env)
        assert result.stdout.strip() == "active", "profile-sync.timer is not active."
    except Exception as e:
        pytest.fail(f"Failed to check timer status: {e}")

def test_adversarial_corpus_filter():
    script_path = "/home/user/deploy/filter_profiles.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    evil_corpus = "/opt/tests/corpora/evil/"
    clean_corpus = "/opt/tests/corpora/clean/"

    if not os.path.isdir(evil_corpus) or not os.path.isdir(clean_corpus):
        pytest.skip("Corpus directories not found, skipping adversarial test.")

    evil_files = [f for f in os.listdir(evil_corpus) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(clean_corpus) if f.endswith('.json')]

    with tempfile.TemporaryDirectory() as temp_out:
        # Test evil corpus
        result_evil = subprocess.run([script_path, evil_corpus, temp_out], capture_output=True, text=True)
        assert result_evil.returncode == 0, f"Script failed on evil corpus: {result_evil.stderr}"

        evil_bypassed = os.listdir(temp_out)
        assert len(evil_bypassed) == 0, f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}"

    with tempfile.TemporaryDirectory() as temp_out:
        # Test clean corpus
        result_clean = subprocess.run([script_path, clean_corpus, temp_out], capture_output=True, text=True)
        assert result_clean.returncode == 0, f"Script failed on clean corpus: {result_clean.stderr}"

        clean_preserved = os.listdir(temp_out)
        clean_modified = set(clean_files) - set(clean_preserved)

        # Verify they are symlinks
        for f in clean_preserved:
            filepath = os.path.join(temp_out, f)
            assert os.path.islink(filepath), f"Clean file {f} was not symlinked."

        assert len(clean_modified) == 0, f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {list(clean_modified)}"