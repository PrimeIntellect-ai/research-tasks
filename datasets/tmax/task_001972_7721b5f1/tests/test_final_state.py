# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_exists():
    assert os.path.isfile("/home/user/classifier.py"), "Classifier script is missing at /home/user/classifier.py"

def test_shared_library_exists():
    assert os.path.isfile("/app/build/libartifact.so"), "Shared library is missing at /app/build/libartifact.so"

def test_benchmark_log_exists():
    assert os.path.isfile("/home/user/benchmark.log"), "Benchmark log is missing at /home/user/benchmark.log"

def test_adversarial_corpus():
    evil_corpus_path = "/app/corpora/evil/"
    clean_corpus_path = "/app/corpora/clean/"

    assert os.path.isdir(evil_corpus_path), f"Evil corpus path {evil_corpus_path} does not exist."
    assert os.path.isdir(clean_corpus_path), f"Clean corpus path {clean_corpus_path} does not exist."

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]

    evil_failures = []
    for filepath in evil_files:
        try:
            result = subprocess.run(
                ["python3", "/home/user/classifier.py", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append((os.path.basename(filepath), output))
        except Exception as e:
            evil_failures.append((os.path.basename(filepath), str(e)))

    clean_failures = []
    for filepath in clean_files:
        try:
            result = subprocess.run(
                ["python3", "/home/user/classifier.py", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append((os.path.basename(filepath), output))
        except Exception as e:
            clean_failures.append((os.path.basename(filepath), str(e)))

    error_message = []
    if evil_failures:
        error_message.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed.")
        error_message.append("Offending evil files: " + ", ".join([f[0] for f in evil_failures[:10]]))
    if clean_failures:
        error_message.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected.")
        error_message.append("Offending clean files: " + ", ".join([f[0] for f in clean_failures[:10]]))

    if error_message:
        pytest.fail("\n".join(error_message))