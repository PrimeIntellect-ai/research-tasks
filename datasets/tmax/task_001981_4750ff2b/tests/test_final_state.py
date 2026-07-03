# test_final_state.py

import os
import re
import pytest

def test_simulate_script_fixed():
    """Check if simulate.py contains the fixed Symplectic Euler implementation."""
    script_path = "/home/user/simulate.py"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    pos_update = "pos = pos + vel * dt"
    vel_update = "vel = vel + acc * dt"

    # Allow for some whitespace variations
    pos_idx = content.find("pos = pos + vel")
    if pos_idx == -1:
        # Try regex
        pos_match = re.search(r'pos\s*\+=\s*vel\s*\*\s*dt|pos\s*=\s*pos\s*\+\s*vel\s*\*\s*dt', content)
        assert pos_match is not None, "Could not find position update in simulate.py"
        pos_idx = pos_match.start()

    vel_idx = content.find("vel = vel + acc")
    if vel_idx == -1:
        vel_match = re.search(r'vel\s*\+=\s*acc\s*\*\s*dt|vel\s*=\s*vel\s*\+\s*acc\s*\*\s*dt', content)
        assert vel_match is not None, "Could not find velocity update in simulate.py"
        vel_idx = vel_match.start()

    assert vel_idx < pos_idx, "simulate.py must update velocity BEFORE position (Symplectic Euler)."

def test_scripts_exist():
    """Ensure that the required scripts exist."""
    assert os.path.isfile("/home/user/analyze.py"), "/home/user/analyze.py is missing."
    assert os.path.isfile("/home/user/pipeline.sh"), "/home/user/pipeline.sh is missing."

def test_results_log():
    """Check the contents of results.log for correctness."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"Missing file: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, "results.log must contain at least 3 lines of output."

    star_line = lines[0]
    ring_line = lines[1]
    match_line = lines[2]

    # Check Star frequency
    star_match = re.search(r'Star frequency:\s*([0-9.]+)', star_line, re.IGNORECASE)
    assert star_match is not None, "Line 1 of results.log must be 'Star frequency: <value>'"
    star_val = float(star_match.group(1))
    assert 1.58 <= star_val <= 1.60, f"Star frequency {star_val} is out of expected range (1.58-1.60)."

    # Check Ring frequency
    ring_match = re.search(r'Ring frequency:\s*([0-9.]+)', ring_line, re.IGNORECASE)
    assert ring_match is not None, "Line 2 of results.log must be 'Ring frequency: <value>'"
    ring_val = float(ring_match.group(1))
    assert 1.41 <= ring_val <= 1.44, f"Ring frequency {ring_val} is out of expected range (1.41-1.44)."

    # Check Hypothesis match
    assert "ring" in match_line.lower(), "Line 3 of results.log must indicate 'ring' as the hypothesis match."
    assert "Hypothesis match:" in match_line, "Line 3 must start with 'Hypothesis match:'"