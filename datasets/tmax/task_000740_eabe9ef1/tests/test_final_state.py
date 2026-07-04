# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def run_pipeline(input_csv, output_csv):
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}. The data processing script must be created."

    # Execute the script
    result = subprocess.run(
        ["bash", script_path, input_csv, output_csv],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed on {input_csv}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(output_csv), f"Script did not create the expected output file: {output_csv}"

def test_pipeline_evil_corpus():
    evil_dir = "/app/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    for f in evil_files:
        input_csv = os.path.join(evil_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_csv = tmp.name

        try:
            run_pipeline(input_csv, output_csv)
            with open(output_csv, 'r') as out_f:
                lines = [line.strip() for line in out_f.readlines() if line.strip()]

            # The evil corpus should have all its data rows dropped, leaving only the header
            if lines != ["id,text_data"]:
                failed_files.append(f)
        finally:
            if os.path.exists(output_csv):
                os.remove(output_csv)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed (failed to drop all malicious rows): {', '.join(failed_files)}"

def test_pipeline_clean_corpus():
    clean_dir = "/app/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for f in clean_files:
        input_csv = os.path.join(clean_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_csv = tmp.name

        try:
            run_pipeline(input_csv, output_csv)
            with open(input_csv, 'r') as in_f:
                expected_lines = [line.strip() for line in in_f.readlines() if line.strip()]
            with open(output_csv, 'r') as out_f:
                actual_lines = [line.strip() for line in out_f.readlines() if line.strip()]

            # The clean corpus should be perfectly preserved
            if actual_lines != expected_lines:
                failed_files.append(f)
        finally:
            if os.path.exists(output_csv):
                os.remove(output_csv)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified (failed to perfectly preserve clean data): {', '.join(failed_files)}"