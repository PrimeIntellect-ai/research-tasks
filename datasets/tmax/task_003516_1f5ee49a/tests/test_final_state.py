# test_final_state.py

import os
import subprocess
import pytest

def test_filter_executable_exists():
    """Test that the compiled filter executable exists."""
    assert os.path.isfile('/home/user/filter'), "/home/user/filter executable is missing."
    assert os.access('/home/user/filter', os.X_OK), "/home/user/filter is not executable."

def test_adversarial_corpus():
    """Test that the filter correctly accepts clean sequences and rejects evil sequences."""
    executable = '/home/user/filter'
    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.fasta')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.fasta')]

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([executable, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([executable, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failures)}")

    assert not clean_failures and not evil_failures, " | ".join(error_msgs)

def test_timeseries_csv_exists():
    """Test that the timeseries.csv file exists."""
    assert os.path.isfile('/home/user/timeseries.csv'), "/home/user/timeseries.csv is missing."

def test_plot_png_exists():
    """Test that the plot.png file exists."""
    assert os.path.isfile('/home/user/plot.png'), "/home/user/plot.png is missing."