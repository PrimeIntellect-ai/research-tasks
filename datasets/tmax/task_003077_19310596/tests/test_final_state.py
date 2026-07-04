# test_final_state.py
import os
import pytest

def test_fixed_output_log_exists():
    """Test that the fixed output log file exists."""
    log_path = "/home/user/fixed_output.log"
    assert os.path.exists(log_path), f"File {log_path} is missing. Ensure you redirected the output."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

def test_fixed_output_log_content():
    """Test that the fixed output log contains the correct execution trace."""
    log_path = "/home/user/fixed_output.log"

    with open(log_path, "r") as f:
        content = f.read().strip()
        lines = content.split('\n')

    assert len(lines) > 0, f"File {log_path} is empty."

    # The special packet should have been detected
    assert any("Special ICMP packet detected!" in line for line in lines), \
        "The special ICMP packet was not detected in the log. Did the program process all packets?"

    # The final line should contain the correct processed count
    last_line = lines[-1]
    assert "Total ICMP packets processed: 2" in last_line, \
        f"Expected the last line to be 'Total ICMP packets processed: 2', but got: '{last_line}'. " \
        "Ensure the deadlock is fixed and all packets are processed."

def test_analyzer_c_fixed():
    """Test that analyzer.c still uses mutexes but fixes the deadlock."""
    analyzer_c = "/home/user/analyzer.c"
    assert os.path.exists(analyzer_c), f"File {analyzer_c} is missing."

    with open(analyzer_c, "r") as f:
        content = f.read()

    assert "pthread_mutex_lock(&log_lock);" in content, \
        "Do not remove the pthread_mutex_lock entirely. Fix the specific deadlock issue."
    assert "pthread_mutex_unlock(&log_lock);" in content, \
        "Missing pthread_mutex_unlock. Ensure you unlock the mutex before returning."