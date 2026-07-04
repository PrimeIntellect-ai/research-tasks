# test_final_state.py
import os
import glob
import subprocess
import time
import pytest

def test_service_composition():
    app_dir = "/home/user/simulation_app"
    start_script = os.path.join(app_dir, "start_services.sh")
    worker_log = os.path.join(app_dir, "worker.log")

    # Clear log if it exists
    if os.path.exists(worker_log):
        os.remove(worker_log)

    # Run start_services.sh
    try:
        subprocess.run(["bash", start_script], cwd=app_dir, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run start_services.sh: {e}")

    # Wait 3 seconds
    time.sleep(3)

    # Execute curl
    try:
        subprocess.run(
            ["curl", "-X", "POST", "http://localhost:5050/submit", "-d", '{"job": "verification_job"}', "-H", "Content-Type: application/json"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to submit job to API: {e.stderr.decode()}")

    # Give worker a moment to process
    time.sleep(2)

    # Check worker.log
    assert os.path.exists(worker_log), f"Worker log {worker_log} was not created."
    with open(worker_log, "r") as f:
        log_contents = f.read()

    assert "Processed verification_job" in log_contents, "Worker did not process the verification job successfully."


def test_adversarial_corpus_classifier():
    classifier_script = "/home/user/trace_classifier.py"
    assert os.path.exists(classifier_script), f"Classifier script {classifier_script} not found."

    clean_corpus = glob.glob("/home/user/corpus/clean/*.csv")
    evil_corpus = glob.glob("/home/user/corpus/evil/*.csv")

    assert len(clean_corpus) > 0, "No clean corpus files found."
    assert len(evil_corpus) > 0, "No evil corpus files found."

    plot_file = "/home/user/latest_plot.png"

    clean_failures = []
    for file in clean_corpus:
        if os.path.exists(plot_file):
            os.remove(plot_file)

        result = subprocess.run(["python3", classifier_script, file], capture_output=True, text=True)
        output = result.stdout.strip()

        if output != "CLEAN":
            clean_failures.append(os.path.basename(file))

        if not os.path.exists(plot_file):
            pytest.fail(f"Plot file {plot_file} was not generated for {file}.")

    evil_failures = []
    for file in evil_corpus:
        if os.path.exists(plot_file):
            os.remove(plot_file)

        result = subprocess.run(["python3", classifier_script, file], capture_output=True, text=True)
        output = result.stdout.strip()

        if output != "EVIL":
            evil_failures.append(os.path.basename(file))

        if not os.path.exists(plot_file):
            pytest.fail(f"Plot file {plot_file} was not generated for {file}.")

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_corpus)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_corpus)} evil bypassed: {', '.join(evil_failures)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))