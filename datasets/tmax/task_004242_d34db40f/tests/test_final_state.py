# test_final_state.py

import os
import subprocess
import tempfile
import filecmp

def test_script_exists():
    script_path = "/home/user/organizer.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_atomic_write_implementation():
    script_path = "/home/user/organizer.py"
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for indications of atomic write pattern
    has_atomic_pattern = any(x in content for x in [
        'os.replace', 
        'os.rename', 
        'shutil.move', 
        'tempfile'
    ])
    assert has_atomic_pattern, "organizer.py does not appear to implement atomic writes (missing os.replace, os.rename, shutil.move, or tempfile)."

def test_clean_corpus():
    script_path = "/home/user/organizer.py"
    clean_dir = "/app/eval_corpora/clean/"

    assert os.path.isdir(clean_dir), "Clean corpus directory missing."
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean files found."

    failed_clean = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(clean_dir, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", script_path, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 0:
                failed_clean.append((filename, f"Exit code {result.returncode} instead of 0"))
                continue

            if not os.path.isfile(output_path):
                failed_clean.append((filename, "Output file was not created"))
                continue

            if not filecmp.cmp(input_path, output_path, shallow=False):
                failed_clean.append((filename, "Output file content does not match input"))
                continue

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files failed. Examples: {failed_clean[:5]}"

def test_evil_corpus():
    script_path = "/home/user/organizer.py"
    evil_dir = "/app/eval_corpora/evil/"

    assert os.path.isdir(evil_dir), "Evil corpus directory missing."
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil files found."

    failed_evil = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(evil_dir, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                ["python3", script_path, input_path, output_path],
                capture_output=True
            )

            if result.returncode != 1:
                failed_evil.append((filename, f"Exit code {result.returncode} instead of 1"))
                continue

            if os.path.exists(output_path):
                failed_evil.append((filename, "Output file was created for an evil input"))
                continue

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil files bypassed rejection. Examples: {failed_evil[:5]}"