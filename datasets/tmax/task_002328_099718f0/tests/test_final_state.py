# test_final_state.py

import os
import json
import math
import subprocess
import tempfile
import pytest

def test_video_analysis_json():
    json_path = "/home/user/video_analysis.json"
    assert os.path.isfile(json_path), f"JSON output missing at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {json_path} is not valid JSON.")

    expected_keys = {"total_frames", "blank_frames", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {set(data.keys())}"

    assert data["total_frames"] == 120, f"Expected total_frames=120, got {data['total_frames']}"
    assert data["blank_frames"] == 18, f"Expected blank_frames=18, got {data['blank_frames']}"

    assert math.isclose(data["ci_lower"], 0.0965, abs_tol=1e-4), f"Expected ci_lower~0.0965, got {data['ci_lower']}"
    assert math.isclose(data["ci_upper"], 0.2256, abs_tol=1e-4), f"Expected ci_upper~0.2256, got {data['ci_upper']}"

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script at {script_path} is not executable."

def test_filter_transcripts_script_exists():
    script_path = "/home/user/filter_transcripts.py"
    assert os.path.isfile(script_path), f"Filter script missing at {script_path}"

def test_adversarial_corpus_filtering():
    script_path = "/home/user/filter_transcripts.py"
    evil_corpus = "/app/test_corpus/evil/"
    clean_corpus = "/app/test_corpus/clean/"

    assert os.path.isdir(evil_corpus), f"Evil corpus missing at {evil_corpus}"
    assert os.path.isdir(clean_corpus), f"Clean corpus missing at {clean_corpus}"

    evil_files = [f for f in os.listdir(evil_corpus) if f.endswith(".txt")]
    clean_files = [f for f in os.listdir(clean_corpus) if f.endswith(".txt")]

    with tempfile.TemporaryDirectory() as evil_out, tempfile.TemporaryDirectory() as clean_out:
        # Run on evil corpus
        result_evil = subprocess.run(
            ["python3", script_path, evil_corpus, evil_out],
            capture_output=True, text=True
        )
        assert result_evil.returncode == 0, f"Script failed on evil corpus:\n{result_evil.stderr}"

        # Run on clean corpus
        result_clean = subprocess.run(
            ["python3", script_path, clean_corpus, clean_out],
            capture_output=True, text=True
        )
        assert result_clean.returncode == 0, f"Script failed on clean corpus:\n{result_clean.stderr}"

        # Check evil output (should be empty)
        evil_out_files = set(os.listdir(evil_out))
        failed_evil = len(evil_out_files)
        total_evil = len(evil_files)

        # Check clean output (should have all files)
        clean_out_files = set(os.listdir(clean_out))
        expected_clean_files = set(clean_files)
        missing_clean = expected_clean_files - clean_out_files
        failed_clean = len(missing_clean)
        total_clean = len(clean_files)

        errors = []
        if failed_evil > 0:
            errors.append(f"{failed_evil} of {total_evil} evil bypassed (e.g. {list(evil_out_files)[:5]})")
        if failed_clean > 0:
            errors.append(f"{failed_clean} of {total_clean} clean modified/dropped (e.g. {list(missing_clean)[:5]})")

        if errors:
            pytest.fail(" | ".join(errors))