# test_final_state.py
import os
import sys

def test_verification_log():
    log_path = "/home/user/workspace/verification.log"
    assert os.path.isfile(log_path), f"Verification log not found at {log_path}"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected verification.log to contain SUCCESS, but got '{content}'"

def test_stats_buffer_fixed():
    sys.path.append("/home/user/workspace")
    try:
        from stats_buffer import SlidingWindowStats
    except ImportError:
        assert False, "Could not import SlidingWindowStats from stats_buffer.py"

    # Test ring buffer fix
    stats = SlidingWindowStats(3)
    stats.add(10)
    stats.add(20)
    stats.add(30)
    stats.add(40)
    assert sorted(stats.buffer) == [20, 30, 40], f"Ring buffer overwrite failed, got {sorted(stats.buffer)}"
    stats.add(50)
    assert sorted(stats.buffer) == [30, 40, 50], f"Ring buffer overwrite failed, got {sorted(stats.buffer)}"

    # Test percentile formula fix
    stats2 = SlidingWindowStats(5)
    for v in [15, 20, 35, 40, 50]:
        stats2.add(v)

    p50 = stats2.get_percentile(50)
    assert p50 == 35.0, f"Percentile formula failed. Expected 35.0, got {p50}"

    p75 = stats2.get_percentile(75)
    assert p75 == 40.0, f"Percentile formula failed. Expected 40.0, got {p75}"