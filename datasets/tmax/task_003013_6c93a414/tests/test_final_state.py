# test_final_state.py

import os
import json

def test_profiling_report():
    report_path = '/home/user/profiling_report.json'
    truth_path = '/home/user/.truth.json'

    assert os.path.isfile(report_path), f"The output file {report_path} was not found."
    assert os.path.isfile(truth_path), f"The truth file {truth_path} is missing."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    with open(truth_path, 'r') as f:
        truth_data = json.load(f)

    expected_keys = ["dominant_frequencies", "latency_kde_peak", "latency_p99", "convergence_n"]
    for key in expected_keys:
        assert key in report_data, f"The key '{key}' is missing from the profiling report."

    # Check dominant_frequencies
    rep_freqs = report_data["dominant_frequencies"]
    truth_freqs = truth_data["dominant_frequencies"]
    assert isinstance(rep_freqs, list) and len(rep_freqs) == 2, "dominant_frequencies must be a list of two elements."
    assert rep_freqs == truth_freqs, f"Expected dominant_frequencies to be {truth_freqs}, but got {rep_freqs}."

    # Check latency_kde_peak
    rep_peak = report_data["latency_kde_peak"]
    truth_peak = truth_data["latency_kde_peak"]
    assert isinstance(rep_peak, (int, float)), "latency_kde_peak must be a number."
    assert abs(rep_peak - truth_peak) <= 0.05, f"Expected latency_kde_peak to be approximately {truth_peak}, but got {rep_peak}."

    # Check latency_p99
    rep_p99 = report_data["latency_p99"]
    truth_p99 = truth_data["latency_p99"]
    assert isinstance(rep_p99, (int, float)), "latency_p99 must be a number."
    assert abs(rep_p99 - truth_p99) <= 0.05, f"Expected latency_p99 to be approximately {truth_p99}, but got {rep_p99}."

    # Check convergence_n
    rep_n = report_data["convergence_n"]
    truth_n = truth_data["convergence_n"]
    assert isinstance(rep_n, int), "convergence_n must be an integer."
    assert rep_n == truth_n, f"Expected convergence_n to be {truth_n}, but got {rep_n}."