# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

FILTER_SCRIPT = "/home/user/api_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_filter_script_exists_and_executable():
    assert os.path.exists(FILTER_SCRIPT), f"Missing filter script at {FILTER_SCRIPT}"
    assert os.path.isfile(FILTER_SCRIPT), f"{FILTER_SCRIPT} is not a file"
    assert os.access(FILTER_SCRIPT, os.X_OK), f"Filter script at {FILTER_SCRIPT} is not executable"

def run_filter(file_path: str) -> list[str]:
    result = subprocess.run(
        [FILTER_SCRIPT, file_path],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0, f"Script failed on {file_path} with stderr: {result.stderr}"
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

def test_clean_corpus_accepted():
    clean_files = list(Path(CLEAN_CORPUS_DIR).glob("*.txt"))
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    bypassed = []
    total_clean = 0

    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        total_clean += len(lines)
        output_lines = run_filter(str(clean_file))

        assert len(output_lines) == len(lines), f"Output line count mismatch for {clean_file.name}"

        for url, out in zip(lines, output_lines):
            if not out.startswith("ACCEPT:"):
                bypassed.append(url)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {total_clean} clean modified/rejected. Offending URLs: {bypassed[:5]}")

def test_evil_corpus_rejected():
    evil_files = list(Path(EVIL_CORPUS_DIR).glob("*.txt"))
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    bypassed = []
    total_evil = 0

    for evil_file in evil_files:
        with open(evil_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        total_evil += len(lines)
        output_lines = run_filter(str(evil_file))

        assert len(output_lines) == len(lines), f"Output line count mismatch for {evil_file.name}"

        for url, out in zip(lines, output_lines):
            if not out.startswith("REJECT:"):
                bypassed.append(url)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {total_evil} evil bypassed. Offending URLs: {bypassed[:5]}")