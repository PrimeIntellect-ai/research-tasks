# test_final_state.py
import os
import time
import subprocess
import pytest

def get_rss_mb(pid):
    """Returns the Resident Set Size (RSS) of a process in Megabytes."""
    try:
        with open(f"/proc/{pid}/statm", "r") as f:
            rss_pages = int(f.read().split()[1])
            page_size = os.sysconf('SC_PAGE_SIZE')
            return rss_pages * page_size / (1024 * 1024)
    except (FileNotFoundError, ProcessLookupError, IndexError):
        return None

def test_memory_leak_fixed():
    """
    Executes the service script and measures memory growth over a period
    to ensure the memory leak has been fixed.
    """
    script_path = "/home/user/service.py"
    assert os.path.isfile(script_path), f"Expected file {script_path} does not exist."

    # Start the service in test mode
    process = subprocess.Popen(["python3", script_path, "--test-mode"])

    try:
        # Wait for warmup (simulating 500 iterations)
        time.sleep(2)

        assert process.poll() is None, "Service process terminated prematurely during warmup."

        mem_start = get_rss_mb(process.pid)
        assert mem_start is not None, "Could not read initial memory usage of the process."

        # Wait for further processing (simulating 5000 iterations)
        time.sleep(10)

        assert process.poll() is None, "Service process terminated prematurely before final memory measurement."

        mem_end = get_rss_mb(process.pid)
        assert mem_end is not None, "Could not read final memory usage of the process."

        growth = mem_end - mem_start

        assert growth <= 2.0, (
            f"Memory leak detected! RSS memory growth was {growth:.2f} MB "
            f"(from {mem_start:.2f} MB to {mem_end:.2f} MB), "
            f"which exceeds the maximum allowed growth of 2.0 MB."
        )

    finally:
        # Clean up the process
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()