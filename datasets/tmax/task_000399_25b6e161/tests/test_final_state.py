# test_final_state.py
import os
import glob
import subprocess
import json
import pytest

def test_adversarial_corpus_sanitizer():
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    sanitizer_dir = "/home/user/sanitizer"
    assert os.path.isdir(sanitizer_dir), f"Sanitizer directory missing at {sanitizer_dir}"

    # Pre-build the Rust project to ensure it compiles and runs smoothly
    build_process = subprocess.run(
        ["cargo", "build"],
        cwd=sanitizer_dir,
        capture_output=True,
        text=True
    )
    assert build_process.returncode == 0, f"Cargo build failed in {sanitizer_dir}:\n{build_process.stderr}"

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(
            ["cargo", "run", "--quiet", "--", evil_file],
            cwd=sanitizer_dir,
            capture_output=True
        )
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    modified_clean = []
    for clean_file in clean_files:
        result = subprocess.run(
            ["cargo", "run", "--quiet", "--", clean_file],
            cwd=sanitizer_dir,
            capture_output=True
        )
        if result.returncode != 0:
            modified_clean.append(os.path.basename(clean_file))

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail(" ; ".join(error_messages))

def test_graph_results_format():
    results_path = "/home/user/graph_results.json"
    assert os.path.isfile(results_path), f"Graph results JSON missing at {results_path}"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {results_path} is not valid JSON.")

    assert "shortest_path" in data, "Missing 'shortest_path' key in results JSON."
    assert "top_centrality" in data, "Missing 'top_centrality' key in results JSON."

    assert isinstance(data["shortest_path"], list), "'shortest_path' must be a list."
    assert isinstance(data["top_centrality"], list), "'top_centrality' must be a list."
    assert len(data["top_centrality"]) == 5, f"Expected 5 nodes in top centrality, found {len(data['top_centrality'])}."

    for item in data["top_centrality"]:
        assert "node" in item, "Centrality item missing 'node' key."
        assert "degree" in item, "Centrality item missing 'degree' key."