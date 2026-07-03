# test_final_state.py

import os
import subprocess
import pytest

def test_telemetry_parser_builds():
    """Verify that the telemetry-parser Makefile has been fixed and builds successfully."""
    vendor_dir = '/app/vendor/telemetry-parser'
    assert os.path.isdir(vendor_dir), f"Directory {vendor_dir} is missing"

    # Run make build
    result = subprocess.run(
        ['make', 'build'],
        cwd=vendor_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"make build failed in {vendor_dir}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Verify the binary was created
    assert os.path.isfile(os.path.join(vendor_dir, 'bin', 'telemetry')), "Binary bin/telemetry was not created by make build"

def test_classifier_executable_exists():
    """Verify the trace_filter executable exists."""
    executable = '/home/user/prof_classifier/trace_filter'
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you compile the Go code?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_classifier_accuracy():
    """Verify the classifier correctly identifies EVIL and CLEAN traces."""
    executable = '/home/user/prof_classifier/trace_filter'
    assert os.path.isfile(executable), "Executable missing, cannot run accuracy tests."

    evil_dir = '/home/user/corpora/evil'
    clean_dir = '/home/user/corpora/clean'

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]

    assert len(evil_files) > 0, "No evil traces found to test."
    assert len(clean_files) > 0, "No clean traces found to test."

    evil_bypassed = []
    clean_rejected = []

    # Test Evil corpus
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        result = subprocess.run([executable, path], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_bypassed.append((f, output))

    # Test Clean corpus
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        result = subprocess.run([executable, path], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_rejected.append((f, output))

    error_msgs = []
    if evil_bypassed:
        bypassed_names = [name for name, _ in evil_bypassed]
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_names)}")
    if clean_rejected:
        rejected_names = [name for name, _ in clean_rejected]
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(rejected_names)}")

    if error_msgs:
        pytest.fail("Classifier errors:\n" + "\n".join(error_msgs))