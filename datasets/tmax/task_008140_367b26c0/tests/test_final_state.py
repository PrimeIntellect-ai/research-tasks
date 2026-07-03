# test_final_state.py

import os
import math
import statistics
import pytest

BASE_DIR = "/home/user/legacy_telemetry"
DATA_DIR = os.path.join(BASE_DIR, "data")
PCAP_FILE = os.path.join(DATA_DIR, "sample.pcap")
RESULT_FILE = os.path.join(BASE_DIR, "result.txt")

def test_sample_pcap_restored():
    """Verify that the sample.pcap file was restored from the git history."""
    assert os.path.isfile(PCAP_FILE), (
        f"The file {PCAP_FILE} is missing. It should have been restored from git history."
    )
    assert os.path.getsize(PCAP_FILE) > 0, (
        f"The file {PCAP_FILE} is empty. Ensure it was properly restored."
    )

def test_result_file_exists():
    """Verify that the result.txt file was generated."""
    assert os.path.isfile(RESULT_FILE), (
        f"The file {RESULT_FILE} is missing. You need to run the pipeline to generate it."
    )

def test_result_file_variance_accurate():
    """Verify that the variance calculated in result.txt is accurate."""
    # Recompute the expected variance based on the generated truth values
    base_val = 100000000.0
    values = [base_val + (i * 0.0001) for i in range(10)]
    expected_variance = statistics.variance(values)

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    try:
        actual_variance = float(content)
    except ValueError:
        pytest.fail(f"The content of {RESULT_FILE} ('{content}') is not a valid float.")

    # The naive variance formula yields 0.0 or something wildly off,
    # so we check for closeness to the true variance.
    assert math.isclose(actual_variance, expected_variance, rel_tol=1e-5), (
        f"The variance in {RESULT_FILE} ({actual_variance}) is incorrect. "
        f"Expected approximately {expected_variance}. "
        "Check analytics.py for catastrophic cancellation issues and ensure reader.py parses all packets correctly."
    )

def test_reader_bug_fixed():
    """Check that reader.py does not contain the original hardcoded buggy slice access."""
    reader_path = os.path.join(BASE_DIR, "reader.py")
    assert os.path.isfile(reader_path), f"{reader_path} is missing."

    with open(reader_path, "r") as f:
        content = f.read()

    # The original bug explicitly checked `if name_bytes[0] == 0:` without checking length
    # A correct implementation would check length first, or decode directly.
    # While we cannot perfectly static-analyze, if the exact buggy line is still there unaltered,
    # it's likely not fixed.
    if "if name_bytes[0] == 0:" in content and "len(name_bytes)" not in content and "try:" not in content:
        pytest.fail("The parsing bug in reader.py appears to be unfixed. It still assumes name_bytes has at least 1 element without checking.")