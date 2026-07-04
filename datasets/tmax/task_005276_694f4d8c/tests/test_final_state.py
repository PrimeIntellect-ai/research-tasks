# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/etl_filter.sh"
CLEAN_CORPUS_DIR = "/app/clean_corpus"
EVIL_CORPUS_DIR = "/app/evil_corpus"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def parse_jsonl(content):
    return [json.loads(line) for line in content.strip().split('\n') if line.strip()]

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.jsonl')]
    assert clean_files, "No clean corpus files found."

    modified_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            input_content = f.read()

        result = subprocess.run(
            [SCRIPT_PATH],
            input=input_content,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            modified_files.append(f"{filename} (script returned non-zero exit code)")
            continue

        input_json = parse_jsonl(input_content)
        try:
            output_json = parse_jsonl(result.stdout)
        except json.JSONDecodeError:
            modified_files.append(f"{filename} (output is not valid JSONL)")
            continue

        if input_json != output_json:
            modified_files.append(filename)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified or rejected: {', '.join(modified_files)}"

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.jsonl')]
    assert evil_files, "No evil corpus files found."

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            input_content = f.read()

        result = subprocess.run(
            [SCRIPT_PATH],
            input=input_content,
            text=True,
            capture_output=True
        )

        output_content = result.stdout.strip()
        if output_content:
            bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed filtering: {', '.join(bypassed_files)}"