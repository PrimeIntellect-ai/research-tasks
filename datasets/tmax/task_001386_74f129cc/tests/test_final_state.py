# test_final_state.py

import os
import re
import pytest

def compute_wer(ref, hyp):
    """Computes Word Error Rate (WER) between reference and hypothesis strings."""
    ref = re.sub(r'[^\w\s]', '', ref.lower()).split()
    hyp = re.sub(r'[^\w\s]', '', hyp.lower()).split()

    d = [[0] * (len(hyp) + 1) for _ in range(len(ref) + 1)]
    for i in range(len(ref) + 1):
        d[i][0] = i
    for j in range(len(hyp) + 1):
        d[0][j] = j

    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            if ref[i - 1] == hyp[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion    = d[i][j - 1] + 1
                deletion     = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    if len(ref) == 0:
        return float('inf')
    return d[len(ref)][len(hyp)] / len(ref)

def test_transcription_accuracy():
    """Check that the transcription meets the WER threshold."""
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript file {transcript_path} is missing."

    with open(transcript_path, "r") as f:
        hyp = f.read().strip()

    ref = "Please update the mailing list server to use port eight zero two five and set the health check timeout to four seconds."

    wer = compute_wer(ref, hyp)
    assert wer <= 0.2, f"Word Error Rate {wer:.2f} exceeds the threshold of 0.2. Transcript was: '{hyp}'"

def test_health_monitor_executable():
    """Check that the health monitor C program is compiled and executable."""
    monitor_path = "/home/user/health_monitor"
    assert os.path.isfile(monitor_path), f"Health monitor executable {monitor_path} is missing."
    assert os.access(monitor_path, os.X_OK), f"Health monitor {monitor_path} is not executable."

def test_deploy_script_exists():
    """Check that the deployment script exists."""
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."

def test_deploy_log_success():
    """Check that the deployment log exists and indicates success."""
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Deployment log {log_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "DEPLOYMENT SUCCESS" in log_content, f"Deployment log does not contain 'DEPLOYMENT SUCCESS'. Log content: {log_content}"