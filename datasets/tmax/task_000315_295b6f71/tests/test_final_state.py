# test_final_state.py

import os
import sys
import glob
import tempfile
import subprocess
import shutil
import pytest

def test_patool_fixed_and_installed():
    """Verify that patoolib can be imported without syntax errors."""
    try:
        import patoolib
    except SyntaxError as e:
        pytest.fail(f"patoolib still contains a SyntaxError: {e}")
    except ImportError as e:
        pytest.fail(f"patoolib is not installed or cannot be imported: {e}")

def test_adversarial_corpus():
    """Verify that the safe_converter.py correctly processes clean and evil corpora."""
    script_path = '/home/user/safe_converter.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    evil_dir = '/app/corpora/evil'
    clean_dir = '/app/corpora/clean'

    evil_zips = glob.glob(os.path.join(evil_dir, '*.zip'))
    clean_zips = glob.glob(os.path.join(clean_dir, '*.zip'))

    assert evil_zips, "No evil zip files found in the corpus."
    assert clean_zips, "No clean zip files found in the corpus."

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for evil_zip in evil_zips:
        with tempfile.TemporaryDirectory() as out_dir:
            result = subprocess.run(
                [sys.executable, script_path, evil_zip, out_dir],
                capture_output=True,
                text=True
            )

            basename = os.path.basename(evil_zip)
            if result.returncode != 1:
                evil_bypassed.append(f"{basename} (exit code {result.returncode} != 1)")
                continue

            if "MALICIOUS" not in result.stdout:
                evil_bypassed.append(f"{basename} (stdout did not contain MALICIOUS)")
                continue

            if os.listdir(out_dir):
                evil_bypassed.append(f"{basename} (files were written to output dir)")
                continue

    # Test Clean Corpus
    for clean_zip in clean_zips:
        with tempfile.TemporaryDirectory() as out_dir:
            result = subprocess.run(
                [sys.executable, script_path, clean_zip, out_dir],
                capture_output=True,
                text=True
            )

            basename = os.path.basename(clean_zip)
            if result.returncode != 0:
                clean_modified.append(f"{basename} (exit code {result.returncode} != 0)")
                continue

            out_file = os.path.join(out_dir, 'converted.txt')
            if not os.path.isfile(out_file):
                clean_modified.append(f"{basename} (converted.txt not created)")
                continue

            with open(out_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic sanity check for concatenated format
            if '--- ' not in content:
                clean_modified.append(f"{basename} (converted.txt missing headers)")
                continue

    # Summarize results
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_zips)} evil bypassed: " + ", ".join(evil_bypassed))
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_zips)} clean modified/failed: " + ", ".join(clean_modified))

    if errors:
        pytest.fail("\n".join(errors))