# test_final_state.py
import os
import subprocess
import pytest

def test_sanitizer_adversarial_corpus():
    sanitizer_dir = "/home/user/sanitizer"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isdir(sanitizer_dir), f"Directory {sanitizer_dir} does not exist."
    assert os.path.isfile(os.path.join(sanitizer_dir, "Cargo.toml")), "Cargo.toml not found in sanitizer dir."

    # Pre-build the project to ensure build errors are caught early and don't pollute runtime output
    build_res = subprocess.run(
        ["cargo", "build", "--release"], 
        cwd=sanitizer_dir, 
        capture_output=True, 
        text=True
    )
    assert build_res.returncode == 0, f"Failed to build the Rust project:\n{build_res.stderr}"

    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])
    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_bypassed = []

    # Test clean corpus
    for cf in clean_files:
        path = os.path.join(clean_dir, cf)
        res = subprocess.run(
            ["cargo", "run", "-q", "--release", "--", path], 
            cwd=sanitizer_dir, 
            capture_output=True, 
            text=True
        )
        stdout = res.stdout.strip()
        if res.returncode != 0 or stdout != "ACCEPT":
            clean_failed.append((cf, res.returncode, stdout))

    # Test evil corpus
    for ef in evil_files:
        path = os.path.join(evil_dir, ef)
        res = subprocess.run(
            ["cargo", "run", "-q", "--release", "--", path], 
            cwd=sanitizer_dir, 
            capture_output=True, 
            text=True
        )
        stdout = res.stdout.strip()
        if res.returncode != 1 or not stdout.startswith("REJECT:"):
            evil_bypassed.append((ef, res.returncode, stdout))

    error_messages = []

    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed:")
        for ef, rc, out in evil_bypassed:
            error_messages.append(f"  {ef} (rc={rc}, stdout={repr(out)})")

    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/failed:")
        for cf, rc, out in clean_failed:
            error_messages.append(f"  {cf} (rc={rc}, stdout={repr(out)})")

    if error_messages:
        pytest.fail("\n".join(error_messages))