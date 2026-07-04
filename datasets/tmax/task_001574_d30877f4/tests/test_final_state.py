# test_final_state.py

import os
import subprocess
from pathlib import Path

def test_incident_frame():
    """Verify the correct frame number is written to incident_frame.txt."""
    frame_txt = Path("/home/user/incident_frame.txt")
    assert frame_txt.is_file(), f"File not found: {frame_txt}"
    content = frame_txt.read_text().strip()
    assert content == "142", f"Expected frame '142', but got '{content}'"

def test_nginx_config():
    """Verify nginx.conf is updated to point to the correct upstream port."""
    conf_path = Path("/home/user/gateway/nginx.conf")
    assert conf_path.is_file(), f"File not found: {conf_path}"
    content = conf_path.read_text()
    assert "proxy_pass http://127.0.0.1:8081;" in content, "nginx.conf does not contain the corrected proxy_pass directive"

def test_classifier_adversarial_corpus():
    """Verify the classifier correctly identifies EVIL and CLEAN corpus files."""
    classifier_path = Path("/home/user/classifier.py")
    assert classifier_path.is_file(), f"Classifier not found at {classifier_path}"

    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")

    clean_failed = []
    evil_failed = []

    # Test clean corpus
    if clean_dir.is_dir():
        clean_files = list(clean_dir.iterdir())
        for f in clean_files:
            if not f.is_file():
                continue
            res = subprocess.run(["python3", str(classifier_path), str(f)], capture_output=True, text=True)
            if res.returncode != 0 or "CLEAN" not in res.stdout:
                clean_failed.append(f.name)

    # Test evil corpus
    if evil_dir.is_dir():
        evil_files = list(evil_dir.iterdir())
        for f in evil_files:
            if not f.is_file():
                continue
            res = subprocess.run(["python3", str(classifier_path), str(f)], capture_output=True, text=True)
            if res.returncode != 1 or "EVIL" not in res.stdout:
                evil_failed.append(f.name)

    total_clean = len(clean_files) if clean_dir.is_dir() else 0
    total_evil = len(evil_files) if evil_dir.is_dir() else 0

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {total_evil} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {total_clean} clean modified/rejected: {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_git_pre_commit_hook():
    """Verify the pre-commit hook blocks evil files and allows clean files."""
    repo_dir = Path("/home/user/gateway")
    hook_path = repo_dir / ".git" / "hooks" / "pre-commit"

    assert hook_path.is_file(), "pre-commit hook does not exist"
    assert os.access(hook_path, os.X_OK), "pre-commit hook is not executable"

    # Test blocking an evil file
    evil_file = repo_dir / "test_evil.req"
    evil_file.write_text("GET /api/v1/../../etc/passwd HTTP/1.1\n")

    subprocess.run(["git", "add", "test_evil.req"], cwd=repo_dir, check=True)
    res_evil = subprocess.run(["git", "commit", "-m", "test evil"], cwd=repo_dir, capture_output=True)

    assert res_evil.returncode != 0, "Git commit succeeded for an EVIL .req file, but it should have been blocked"

    # Clean up evil file
    subprocess.run(["git", "rm", "-f", "test_evil.req"], cwd=repo_dir, check=True)

    # Test allowing a clean file
    clean_file = repo_dir / "test_clean.req"
    clean_file.write_text("GET /index.html HTTP/1.1\n")

    subprocess.run(["git", "add", "test_clean.req"], cwd=repo_dir, check=True)
    res_clean = subprocess.run(["git", "commit", "-m", "test clean"], cwd=repo_dir, capture_output=True)

    assert res_clean.returncode == 0, "Git commit failed for a CLEAN .req file, but it should have been allowed"