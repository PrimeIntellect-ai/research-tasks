# test_final_state.py
import os
import re
import numpy as np

def test_clean_words_exists():
    """Ensure the clean_words.txt file was created."""
    assert os.path.isfile("/home/user/clean_words.txt"), "The file /home/user/clean_words.txt is missing."

def test_analysis_report_exists():
    """Ensure the analysis_report.txt file was created."""
    assert os.path.isfile("/home/user/analysis_report.txt"), "The file /home/user/analysis_report.txt is missing."

def test_metrics():
    """Check that the reported mean and Bootstrap SEM are accurate."""
    report_path = "/home/user/analysis_report.txt"
    words_path = "/home/user/clean_words.txt"

    with open(words_path, 'r') as f:
        words = [line.strip() for line in f if line.strip()]

    assert len(words) > 0, "clean_words.txt is empty, no words extracted."

    lengths = [len(w) for w in words]
    theoretical_sem = np.std(lengths, ddof=1) / np.sqrt(len(lengths))
    actual_mean = np.mean(lengths)

    with open(report_path, 'r') as f:
        content = f.read()

    mean_match = re.search(r'Mean_Length=([0-9.]+)', content)
    assert mean_match, "Mean_Length not found in analysis_report.txt in the correct format."
    agent_mean = float(mean_match.group(1))

    agent_sem_match = re.search(r'Bootstrap_SEM=([0-9.]+)', content)
    assert agent_sem_match, "Bootstrap_SEM not found in analysis_report.txt in the correct format."
    agent_sem = float(agent_sem_match.group(1))

    # Check mean length accuracy
    assert abs(agent_mean - actual_mean) < 0.01, f"Reported Mean_Length {agent_mean} does not match the actual mean length {actual_mean:.4f} of words in clean_words.txt."

    # Check Bootstrap SEM accuracy using the metric threshold
    error = abs(agent_sem - theoretical_sem) / theoretical_sem
    score = max(0.0, 1.0 - (error / 0.10))

    assert score >= 0.8, f"Score {score:.2f} is below threshold 0.8. Reported Bootstrap_SEM: {agent_sem}, Theoretical SEM: {theoretical_sem:.4f}, Relative Error: {error:.4f}"