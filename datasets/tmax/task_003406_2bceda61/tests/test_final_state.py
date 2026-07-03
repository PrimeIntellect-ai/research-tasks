# test_final_state.py

import os
import json
import subprocess
import tempfile
import shutil
import pytest

def test_vendored_package_fixed():
    go_mod_path = "/app/vendored/bluemonday/go.mod"
    assert os.path.exists(go_mod_path), f"Vendored go.mod not found at {go_mod_path}"

    with open(go_mod_path, "r") as f:
        content = f.read()

    assert "module github.com/microcosm-cc/bluemondayy" not in content, "The go.mod file still has the perturbed module name 'bluemondayy'"
    assert "module github.com/microcosm-cc/bluemonday" in content, "The go.mod file should have the correct module name 'bluemonday'"

def test_pipeline_execution():
    pipeline_dir = "/home/user/pipeline"
    go_file = os.path.join(pipeline_dir, "prepare_data.go")

    # Fallback to /home/user/prepare_data.go if not in pipeline dir
    if not os.path.exists(go_file) and os.path.exists("/home/user/prepare_data.go"):
        go_file = "/home/user/prepare_data.go"
        pipeline_dir = "/home/user"

    assert os.path.exists(go_file), f"Go program not found at {go_file}"

    clean_corpus = "/home/user/corpora/clean"
    evil_corpus = "/home/user/corpora/evil"

    with tempfile.TemporaryDirectory() as clean_out, \
         tempfile.TemporaryDirectory() as evil_out, \
         tempfile.TemporaryDirectory() as metrics_dir:

        clean_metrics = os.path.join(metrics_dir, "clean_metrics.json")
        evil_metrics = os.path.join(metrics_dir, "evil_metrics.json")

        # Run on clean corpus
        cmd_clean = [
            "go", "run", go_file,
            "--corpus", clean_corpus,
            "--out", clean_out,
            "--metrics", clean_metrics
        ]
        res_clean = subprocess.run(cmd_clean, cwd=pipeline_dir, capture_output=True, text=True)
        assert res_clean.returncode == 0, f"Go program failed on clean corpus:\n{res_clean.stderr}"

        # Run on evil corpus
        cmd_evil = [
            "go", "run", go_file,
            "--corpus", evil_corpus,
            "--out", evil_out,
            "--metrics", evil_metrics
        ]
        res_evil = subprocess.run(cmd_evil, cwd=pipeline_dir, capture_output=True, text=True)
        assert res_evil.returncode == 0, f"Go program failed on evil corpus:\n{res_evil.stderr}"

        # Validate clean corpus output
        clean_files_expected = set(os.listdir(clean_corpus))
        clean_files_actual = set(os.listdir(clean_out))

        missing_clean = clean_files_expected - clean_files_actual
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_files_expected)} clean files modified/rejected: {', '.join(missing_clean)}"

        # Validate evil corpus output
        evil_files_expected = set(os.listdir(evil_corpus))
        evil_files_actual = set(os.listdir(evil_out))

        bypassed_evil = evil_files_actual.intersection(evil_files_expected)
        assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files_expected)} evil files bypassed: {', '.join(bypassed_evil)}"
        assert len(evil_files_actual) == 0, "Evil output directory should be empty"

        # Validate metrics files
        assert os.path.exists(clean_metrics), "Clean metrics JSON not created"
        with open(clean_metrics, "r") as f:
            clean_data = json.load(f)
        assert clean_data.get("processed_count") == len(clean_files_expected), "Incorrect processed_count in clean metrics"
        assert clean_data.get("accepted_count") == len(clean_files_expected), "Incorrect accepted_count in clean metrics"
        assert "duration_ms" in clean_data, "duration_ms missing in clean metrics"

        assert os.path.exists(evil_metrics), "Evil metrics JSON not created"
        with open(evil_metrics, "r") as f:
            evil_data = json.load(f)
        assert evil_data.get("processed_count") == len(evil_files_expected), "Incorrect processed_count in evil metrics"
        assert evil_data.get("accepted_count") == 0, "Incorrect accepted_count in evil metrics"
        assert "duration_ms" in evil_data, "duration_ms missing in evil metrics"