# test_final_state.py

import os
import subprocess
import json
import glob
import pytest

PROCESSOR_BIN = "/home/user/processor"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
PIPELINE_SCRIPT = "/home/user/run_pipeline.sh"

def test_processor_exists_and_executable():
    assert os.path.isfile(PROCESSOR_BIN), f"Processor binary {PROCESSOR_BIN} does not exist."
    assert os.access(PROCESSOR_BIN, os.X_OK), f"Processor binary {PROCESSOR_BIN} is not executable."

def test_pipeline_script_exists_and_executable():
    assert os.path.isfile(PIPELINE_SCRIPT), f"Pipeline script {PIPELINE_SCRIPT} does not exist."
    assert os.access(PIPELINE_SCRIPT, os.X_OK), f"Pipeline script {PIPELINE_SCRIPT} is not executable."

def run_processor(input_data: str) -> str:
    result = subprocess.run(
        [PROCESSOR_BIN],
        input=input_data,
        text=True,
        capture_output=True,
        timeout=5
    )
    return result.stdout

def test_adversarial_corpus_clean():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.jsonl"))
    assert clean_files, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    modified_files = []

    for file_path in clean_files:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            stdout = run_processor(line + "\n")
            output_lines = [l for l in stdout.split("\n") if l.strip()]

            if len(output_lines) != 1:
                modified_files.append(os.path.basename(file_path))
                break

            out_line = output_lines[0]
            expected_val = f"{record['value']:.2f}"

            if not out_line.startswith("<Reading>") or not out_line.endswith("</Reading>"):
                modified_files.append(os.path.basename(file_path))
                break

            if f"<ID>{record['id']}</ID>" not in out_line or \
               f"<Type>{record['sensor']}</Type>" not in out_line or \
               f"<Val>{expected_val}</Val>" not in out_line or \
               f"<Meta>{record['meta']}</Meta>" not in out_line:
                modified_files.append(os.path.basename(file_path))
                break

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")

def test_adversarial_corpus_evil():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.jsonl"))
    assert evil_files, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    bypassed_files = []

    for file_path in evil_files:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            if not line.strip():
                continue

            stdout = run_processor(line + "\n")
            output_lines = [l for l in stdout.split("\n") if l.strip()]

            if len(output_lines) > 0:
                if os.path.basename(file_path) not in bypassed_files:
                    bypassed_files.append(os.path.basename(file_path))
                break

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")