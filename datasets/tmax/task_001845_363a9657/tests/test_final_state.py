# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def run_filter(script_path: Path, target_file: Path) -> str:
    result = subprocess.run(
        ["python3", str(script_path), str(target_file)],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_artifact_filter_exists():
    script_path = Path("/home/user/artifact_filter.py")
    assert script_path.exists(), f"Script missing at {script_path}"
    assert script_path.is_file(), f"Path {script_path} is not a file"

def test_clean_corpus_classification():
    script_path = Path("/home/user/artifact_filter.py")
    clean_dir = Path("/app/corpora/clean")
    assert clean_dir.exists() and clean_dir.is_dir(), "Clean corpus directory missing."

    json_files = list(clean_dir.glob("*.json"))
    assert len(json_files) > 0, "No JSON files in clean corpus."

    failures = []
    for json_file in json_files:
        output = run_filter(script_path, json_file)
        if output != "CLEAN":
            failures.append(f"{json_file.name} (output: {output!r})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(json_files)} clean files modified/rejected (expected CLEAN): {', '.join(failures)}")

def test_evil_corpus_classification():
    script_path = Path("/home/user/artifact_filter.py")
    evil_dir = Path("/app/corpora/evil")
    assert evil_dir.exists() and evil_dir.is_dir(), "Evil corpus directory missing."

    json_files = list(evil_dir.glob("*.json"))
    assert len(json_files) > 0, "No JSON files in evil corpus."

    failures = []
    for json_file in json_files:
        output = run_filter(script_path, json_file)
        if output != "EVIL":
            failures.append(f"{json_file.name} (output: {output!r})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(json_files)} evil files bypassed (expected EVIL): {', '.join(failures)}")