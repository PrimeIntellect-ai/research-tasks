# test_final_state.py

import os
import subprocess
import pytest

def test_astro_core_fixed_and_installed():
    calc_py = '/app/vendored/astro_core/astro_core/calc.py'
    assert os.path.isfile(calc_py), f"File missing: {calc_py}"

    with open(calc_py, 'r') as f:
        content = f.read()

    assert 'imprt numpy' not in content, "The deliberate typo 'imprt numpy' is still in calc.py"
    assert 'import numpy' in content, "The import statement for numpy is missing or incorrect in calc.py"

    # Try to import the package to verify it's installed correctly
    try:
        from astro_core.calc import compute_derivative
    except ImportError as e:
        pytest.fail(f"Failed to import astro_core. Make sure it is installed. Error: {e}")

def test_classifier_script_exists():
    script_path = '/home/user/classify.py'
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

def test_adversarial_corpus():
    script_path = '/home/user/classify.py'
    clean_dir = '/home/user/data/clean'
    evil_dir = '/home/user/data/evil'

    assert os.path.isdir(clean_dir), f"Clean directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.h5')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.h5')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    failed_clean = []
    for f in clean_files:
        result = subprocess.run(['python3', script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        result = subprocess.run(['python3', script_path, f], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(f))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))