# test_final_state.py

import os
import subprocess
import tempfile
import time
import pytest

FILTER_BIN = "/home/user/filter_manifest"
PIPELINE_SCRIPT = "/home/user/run_pipeline.sh"

def test_executables_exist():
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} does not exist."
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable."
    assert os.path.isfile(PIPELINE_SCRIPT), f"{PIPELINE_SCRIPT} does not exist."
    assert os.access(PIPELINE_SCRIPT, os.X_OK), f"{PIPELINE_SCRIPT} is not executable."

def test_clean_corpus():
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus dir {clean_dir} missing"

    bin_files = [f for f in os.listdir(clean_dir) if f.endswith('.bin')]
    assert bin_files, "No .bin files found in clean corpus"

    failed = []
    for bin_file in bin_files:
        input_path = os.path.join(clean_dir, bin_file)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_out:
            output_path = tmp_out.name

        try:
            subprocess.run(
                [FILTER_BIN, clean_dir, input_path, output_path],
                check=True,
                capture_output=True
            )

            with open(input_path, 'rb') as f_in, open(output_path, 'rb') as f_out:
                in_data = f_in.read()
                out_data = f_out.read()

            if in_data != out_data:
                failed.append(bin_file)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not failed, f"{len(failed)} of {len(bin_files)} clean modified: {', '.join(failed)}"

def test_evil_corpus():
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus dir {evil_dir} missing"

    bin_files = [f for f in os.listdir(evil_dir) if f.endswith('.bin')]
    assert bin_files, "No .bin files found in evil corpus"

    failed = []
    for bin_file in bin_files:
        input_path = os.path.join(evil_dir, bin_file)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_out:
            output_path = tmp_out.name

        try:
            subprocess.run(
                [FILTER_BIN, evil_dir, input_path, output_path],
                check=True,
                capture_output=True
            )

            with open(output_path, 'rb') as f_out:
                out_data = f_out.read()

            if out_data != b"BKP_MNFS":
                failed.append(bin_file)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not failed, f"{len(failed)} of {len(bin_files)} evil bypassed: {', '.join(failed)}"

def test_pipeline_end_to_end():
    received_manifest = "/app/services/received_manifest.bin"
    if os.path.exists(received_manifest):
        os.remove(received_manifest)

    subprocess.run([PIPELINE_SCRIPT], check=True, timeout=10)

    time.sleep(1) # Allow storage service to flush

    assert os.path.isfile(received_manifest), f"{received_manifest} was not created by the pipeline."

    with open(received_manifest, 'rb') as f:
        data = f.read()

    assert data.startswith(b"BKP_MNFS"), "Received manifest does not have correct header."