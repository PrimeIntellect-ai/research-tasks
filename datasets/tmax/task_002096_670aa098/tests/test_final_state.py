# test_final_state.py

import os
import sys
import json
import time
import importlib.util
import subprocess
import pytest

TARGET_DIR = "/home/user/build_cache_optimizer"
INTERVAL_CACHE_PATH = os.path.join(TARGET_DIR, "interval_cache.py")
TEST_PROPERTIES_PATH = os.path.join(TARGET_DIR, "test_properties.py")
BENCHMARK_PATH = os.path.join(TARGET_DIR, "benchmark.py")
METRICS_PATH = os.path.join(TARGET_DIR, "bench_metrics.json")

def test_directory_and_files_exist():
    assert os.path.isdir(TARGET_DIR), f"Directory {TARGET_DIR} does not exist."
    for filepath in [INTERVAL_CACHE_PATH, TEST_PROPERTIES_PATH, BENCHMARK_PATH, METRICS_PATH]:
        assert os.path.isfile(filepath), f"File {filepath} does not exist."

def test_interval_cache_functionality():
    sys.path.insert(0, TARGET_DIR)
    try:
        from interval_cache import IntervalCache
    except ImportError as e:
        pytest.fail(f"Could not import IntervalCache from interval_cache.py: {e}")

    cache = IntervalCache()
    cache.add_interval(1, 5)
    cache.add_interval(2, 6)
    cache.add_interval(8, 10)
    cache.add_interval(10, 15)

    merged = cache.get_merged_intervals()
    assert merged == [(1, 6), (8, 15)], f"Expected [(1, 6), (8, 15)], got {merged}"

    # Additional test for disjointness and sorting
    cache2 = IntervalCache()
    cache2.add_interval(10, 12)
    cache2.add_interval(1, 3)
    cache2.add_interval(2, 4)
    cache2.add_interval(5, 7)
    assert cache2.get_merged_intervals() == [(1, 4), (5, 7), (10, 12)]

def test_interval_cache_performance():
    sys.path.insert(0, TARGET_DIR)
    from interval_cache import IntervalCache

    cache = IntervalCache()
    # Add 200,000 intervals
    # To avoid O(N^2) insertion time, we should just add them, then merge.
    # The requirement says O(N log N) for N intervals.
    for i in range(200000, 0, -1):
        cache.add_interval(i, i + 2)

    start_time = time.time()
    merged = cache.get_merged_intervals()
    duration = time.time() - start_time

    assert duration < 2.0, f"Performance test failed: took {duration:.2f} seconds, expected < 2.0 seconds."
    assert len(merged) == 1
    assert merged[0] == (1, 200002)

def test_bench_metrics_format():
    with open(METRICS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("bench_metrics.json is not valid JSON.")

    assert "time_seconds" in data, "Key 'time_seconds' missing from bench_metrics.json."
    assert isinstance(data["time_seconds"], float), "'time_seconds' must be a float."

def test_property_tests_pass():
    # Run the student's property tests using pytest
    result = subprocess.run(["pytest", TEST_PROPERTIES_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Property tests failed:\n{result.stdout}\n{result.stderr}"