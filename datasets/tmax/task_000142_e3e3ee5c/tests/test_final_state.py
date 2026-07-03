# test_final_state.py

import os
import shutil
import tempfile
import subprocess
import pytest

def test_doc_unpack_fixed_and_installed():
    """
    Validates that Phase 1 is complete: the doc-unpack tool is fixed and installed.
    """
    bin_path = "/usr/local/bin/doc-unpack"
    assert os.path.isfile(bin_path), f"The doc-unpack binary is missing at {bin_path}. Did you run 'make install'?"
    assert os.access(bin_path, os.X_OK), f"The doc-unpack binary at {bin_path} is not executable."

def test_adversarial_corpus_filtering():
    """
    Validates Phase 2: the filter_docs.sh script correctly preserves clean bundles
    and rejects evil bundles.
    """
    script_path = "/home/user/filter_docs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    with tempfile.TemporaryDirectory() as mixed_dir, tempfile.TemporaryDirectory() as output_dir:
        clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.tar.gz')]
        evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.tar.gz')]

        # Populate mixed directory
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(mixed_dir, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(mixed_dir, f))

        # Run the student's script
        result = subprocess.run(
            ["bash", script_path, mixed_dir, output_dir],
            capture_output=True,
            text=True
        )

        # Output subdirectories representing extracted accepted bundles
        output_subdirs = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]

        bypassed_evil = []
        for f in evil_files:
            base_name = f.replace('.tar.gz', '')
            # If the output directory contains the base name or full file name as a subdirectory, it bypassed the filter
            if any(d == base_name or d == f for d in output_subdirs):
                bypassed_evil.append(f)

        modified_clean = []
        for f in clean_files:
            base_name = f.replace('.tar.gz', '')
            # If the output directory DOES NOT contain the base name or full file name, it was modified/rejected
            if not any(d == base_name or d == f for d in output_subdirs):
                modified_clean.append(f)

        errors = []
        if bypassed_evil:
            errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
        if modified_clean:
            errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

        if errors:
            pytest.fail(" | ".join(errors) + f"\n\nScript STDOUT:\n{result.stdout}\n\nScript STDERR:\n{result.stderr}")