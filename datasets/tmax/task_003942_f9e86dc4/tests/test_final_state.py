# test_final_state.py

import os
import subprocess
import tarfile
import tempfile
import glob
import pytest

def test_pigz_compiled_and_installed():
    """Test that pigz is compiled and installed correctly."""
    pigz_path = "/home/user/bin/pigz"
    assert os.path.isfile(pigz_path), f"pigz binary not found at {pigz_path}"
    assert os.access(pigz_path, os.X_OK), f"pigz binary at {pigz_path} is not executable"

    result = subprocess.run([pigz_path, "--version"], capture_output=True, text=True)
    assert "pigz 2.8" in result.stdout or "pigz 2.8" in result.stderr, "pigz version is not 2.8 or execution failed"

def test_script_exists():
    """Test that the sanitize_backup.sh script exists."""
    script_path = "/home/user/sanitize_backup.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_clean_corpus():
    """Test that the script properly processes the clean corpus."""
    script_path = "/home/user/sanitize_backup.sh"
    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.tar.gz"))

    assert len(clean_files) > 0, "No clean corpus files found."

    modified_clean = []

    for input_file in clean_files:
        basename = os.path.basename(input_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output.tar.gz")
            res = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True)

            if res.returncode != 0 or not os.path.isfile(output_file):
                modified_clean.append(f"{basename} (script failed or no output)")
                continue

            extract_dir = os.path.join(tmpdir, "extracted")
            os.makedirs(extract_dir)
            with tarfile.open(output_file, "r:gz") as tar:
                tar.extractall(path=extract_dir)

            # Check expected clean state
            safe_txt = os.path.join(extract_dir, "docs", "safe.txt")
            safe_link = os.path.join(extract_dir, "docs", "safelink")
            nested_internal_dir = os.path.join(extract_dir, "docs", "nested", "internal")
            nested_safe_txt = os.path.join(nested_internal_dir, "docs", "safe.txt")
            nested_tar = os.path.join(extract_dir, "docs", "nested", "internal.tar.gz")

            is_clean = True
            if not os.path.isfile(safe_txt):
                is_clean = False
            if not os.path.islink(safe_link):
                is_clean = False
            if not os.path.isdir(nested_internal_dir):
                is_clean = False
            if not os.path.isfile(nested_safe_txt):
                is_clean = False
            if os.path.exists(nested_tar):
                is_clean = False

            if not is_clean:
                modified_clean.append(basename)

    if modified_clean:
        pytest.fail(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

def test_evil_corpus():
    """Test that the script properly sanitizes the evil corpus."""
    script_path = "/home/user/sanitize_backup.sh"
    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.tar.gz"))

    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_evil = []

    for input_file in evil_files:
        basename = os.path.basename(input_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output.tar.gz")
            res = subprocess.run(["bash", script_path, input_file, output_file], capture_output=True)

            if res.returncode != 0 or not os.path.isfile(output_file):
                bypassed_evil.append(f"{basename} (script failed or no output)")
                continue

            extract_dir = os.path.join(tmpdir, "extracted")
            os.makedirs(extract_dir)
            with tarfile.open(output_file, "r:gz") as tar:
                tar.extractall(path=extract_dir)

            # Check expected sanitized state
            bad_txt = os.path.join(extract_dir, "payload", "bad.txt")
            abs_link = os.path.join(extract_dir, "payload", "abs_link")
            rel_link = os.path.join(extract_dir, "payload", "rel_link")
            nested_bomb_dir = os.path.join(extract_dir, "payload", "deep", "hidden_evil")
            root_link = os.path.join(nested_bomb_dir, "payload", "nested_bomb", "root_link")
            nested_tar = os.path.join(extract_dir, "payload", "deep", "hidden_evil.tar.gz")

            bypassed = False
            if not os.path.isfile(bad_txt):
                bypassed = True # legitimate file was removed
            if os.path.exists(abs_link) or os.path.islink(abs_link):
                bypassed = True # malicious link preserved
            if os.path.exists(rel_link) or os.path.islink(rel_link):
                bypassed = True # malicious link preserved
            if os.path.exists(root_link) or os.path.islink(root_link):
                bypassed = True # nested malicious link preserved
            if os.path.exists(nested_tar):
                bypassed = True # nested tar not removed

            if bypassed:
                bypassed_evil.append(basename)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")