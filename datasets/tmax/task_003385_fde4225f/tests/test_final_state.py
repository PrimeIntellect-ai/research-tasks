# test_final_state.py

import os
import subprocess
import time
import struct
import pytest

def test_required_files_exist():
    """Check that the user created the required files and they have the right permissions."""
    assert os.path.exists("/home/user/fast_filter.c"), "/home/user/fast_filter.c is missing."
    assert os.path.exists("/home/user/build_and_test.sh"), "/home/user/build_and_test.sh is missing."
    assert os.access("/home/user/build_and_test.sh", os.X_OK), "/home/user/build_and_test.sh is not executable."

    assert os.path.exists("/home/user/fast_filter"), "Compiled binary /home/user/fast_filter is missing."
    assert os.access("/home/user/fast_filter", os.X_OK), "/home/user/fast_filter is not executable."

    assert os.path.exists("/home/user/filtered.log"), "Output file /home/user/filtered.log is missing."

def test_fast_filter_correctness_and_performance():
    """Generate a new test file, run the agent's filter, and verify performance and correctness."""
    eval_bin = "/tmp/eval_events.bin"

    # 1. Generate verification data
    try:
        subprocess.run(["/app/bin/fs_event_gen", "999", eval_bin], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to generate test data with fs_event_gen: {e.stderr.decode(errors='ignore')}")

    assert os.path.exists(eval_bin), f"Test data file {eval_bin} was not created."

    # 2. Run agent's tool and measure time
    start = time.perf_counter()
    result = subprocess.run(
        ["/home/user/fast_filter", eval_bin],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )
    elapsed = time.perf_counter() - start

    assert result.returncode == 0, f"Agent binary crashed or returned non-zero. Stderr: {result.stderr.decode(errors='ignore')}"
    output = result.stdout

    # 3. Compute the golden set
    golden_lines = []
    with open(eval_bin, "rb") as f:
        while True:
            hdr = f.read(14)
            if not hdr:
                break
            if len(hdr) < 14:
                break  # Incomplete header at end of file

            ts, ev_type, plen = struct.unpack("<QIH", hdr)
            path = f.read(plen)

            # Filter condition: event type 3 and path ends with '.conf'
            if ev_type == 3 and path.endswith(b".conf"):
                golden_lines.append(path)

    golden_output = b"\n".join(golden_lines)
    if golden_lines:
        golden_output += b"\n"

    # 4. Assertions
    assert output == golden_output, "Output from /home/user/fast_filter does not match the expected filtered data."
    assert elapsed <= 0.25, f"Execution time {elapsed:.3f}s exceeded threshold of 0.25s."