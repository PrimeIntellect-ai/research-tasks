# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/evaluate_requests.py"
CLEAN_CORPUS = "/app/hidden_corpus/clean/urls.txt"
EVIL_CORPUS = "/app/hidden_corpus/evil/urls.txt"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."

def test_legacy_router_installed():
    try:
        # Check if the package can be imported in the current Python 3 environment
        result = subprocess.run(
            ["python3", "-c", "import legacy_router"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Failed to import legacy_router in Python 3: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Error checking legacy_router installation: {e}")

def run_script(corpus_path):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, corpus_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split("\n")

def test_clean_corpus_accepted():
    assert os.path.isfile(CLEAN_CORPUS), f"Clean corpus {CLEAN_CORPUS} is missing."
    with open(CLEAN_CORPUS, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    num_urls = len(urls)

    outputs = run_script(CLEAN_CORPUS)
    outputs = [o.strip() for o in outputs if o.strip()]

    assert len(outputs) == num_urls, f"Expected {num_urls} outputs, got {len(outputs)}."

    rejected = [i for i, out in enumerate(outputs) if out != "ACCEPT"]
    if rejected:
        offending_urls = [urls[i] for i in rejected]
        pytest.fail(f"{len(rejected)} of {num_urls} clean URLs were rejected/modified. Offending URLs: {offending_urls}")

def test_evil_corpus_rejected():
    assert os.path.isfile(EVIL_CORPUS), f"Evil corpus {EVIL_CORPUS} is missing."
    with open(EVIL_CORPUS, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    num_urls = len(urls)

    outputs = run_script(EVIL_CORPUS)
    outputs = [o.strip() for o in outputs if o.strip()]

    assert len(outputs) == num_urls, f"Expected {num_urls} outputs, got {len(outputs)}."

    accepted = [i for i, out in enumerate(outputs) if out != "REJECT"]
    if accepted:
        offending_urls = [urls[i] for i in accepted]
        pytest.fail(f"{len(accepted)} of {num_urls} evil URLs bypassed the filter. Offending URLs: {offending_urls}")