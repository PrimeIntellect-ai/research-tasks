# test_final_state.py
import os
import subprocess
import re

def test_syscall_storm_fixed():
    """
    Runs the uptime tracker with strace to count select/poll calls.
    Threshold is <= 1005.
    """
    cmd = [
        "strace", "-e", "select,poll,pselect6,ppoll", "-c", 
        "python", "/home/user/monitor/uptime_tracker.py", "--simulate", "1000000"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        # If strace is not available, we fall back to static analysis of the fix
        with open("/app/vendored/pingspinner/core.py", "r") as f:
            content = f.read()
            assert "0.0" not in content or "select.select([sock], [], [], 0.0)" not in content, \
                "Syscall storm not fixed: select.select still uses 0.0 timeout spinloop."
        return

    stderr = result.stderr
    syscall_count = 0

    # Parse strace -c output
    # Format typically: % time     seconds  usecs/call     calls    errors syscall
    for line in stderr.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[-1] in ("select", "poll", "pselect6", "ppoll"):
            try:
                calls = int(parts[3])
                syscall_count += calls
            except ValueError:
                pass

    assert syscall_count <= 1005, f"Syscall count {syscall_count} exceeds threshold of 1005. The spinloop is likely not fully fixed."

def test_precision_and_boundary_fixes():
    """
    Checks that the precision loss and off-by-one errors are fixed in uptime_tracker.py.
    """
    tracker_path = "/home/user/monitor/uptime_tracker.py"
    assert os.path.isfile(tracker_path), f"Missing monitor script at {tracker_path}"

    with open(tracker_path, "r") as f:
        content = f.read()

    # Check for math.fsum or Decimal usage to fix IEEE 754 precision loss
    has_fsum = "fsum" in content
    has_decimal = "Decimal" in content
    assert has_fsum or has_decimal, "Precision loss not fixed: neither math.fsum nor Decimal is used for accumulation."

    # Check for the off-by-one window boundary fix (pop(1) changed to pop(0))
    assert "pop(1)" not in content, "Off-by-one boundary error not fixed: window still pops index 1."

def test_pingspinner_core_fix():
    """
    Checks that the pingspinner core.py has been modified to properly block.
    """
    core_path = "/app/vendored/pingspinner/core.py"
    assert os.path.isfile(core_path), f"Missing vendored library file at {core_path}"

    with open(core_path, "r") as f:
        content = f.read()

    # The original had select.select([sock], [], [], 0.0)
    # The fix should use a calculated remaining timeout instead of 0.0
    assert "select.select([sock], [], [], 0.0)" not in content, "The select.select call still uses a hardcoded 0.0 timeout spinloop."