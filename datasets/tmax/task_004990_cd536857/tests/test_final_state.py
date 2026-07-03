# test_final_state.py

import os
import glob
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_filter_script_exists():
    path = "/home/user/filter.sh"
    assert os.path.isfile(path), f"Expected {path} to exist."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_adversarial_corpus_evil():
    path = "/home/user/filter.sh"
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.fasta"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    bypassed = []
    for f in evil_files:
        result = subprocess.run([path, f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 1:
            bypassed.append(os.path.basename(f))

    assert len(bypassed) == 0, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed[:5])}"

def test_adversarial_corpus_clean():
    path = "/home/user/filter.sh"
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.fasta"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."

    modified = []
    for f in clean_files:
        result = subprocess.run([path, f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            modified.append(os.path.basename(f))

    assert len(modified) == 0, f"{len(modified)} of {len(clean_files)} clean modified (rejected): {', '.join(modified[:5])}"

def test_end_to_end_pipeline():
    # Submit a request to the nginx proxy
    url = "http://localhost:8080/submit"
    fasta_payload = b">test_seq\nATGCATGC"

    req = urllib.request.Request(url, data=fasta_payload, method="POST")
    req.add_header("Content-Type", "text/plain")

    try:
        response = urllib.request.urlopen(req, timeout=5)
        assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to submit request to {url}: {e}")

    # Wait for the worker to process the job and write to /app/results.log
    results_file = "/app/results.log"
    max_retries = 10
    found = False
    for _ in range(max_retries):
        if os.path.exists(results_file):
            with open(results_file, "r") as f:
                content = f.read()
                if "test_seq" in content or "ATGC" in content or len(content.strip()) > 0:
                    found = True
                    break
        time.sleep(0.5)

    assert found, f"Worker did not process the job or failed to write output to {results_file}."