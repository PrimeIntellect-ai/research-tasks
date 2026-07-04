# test_final_state.py
import os
import math

def test_center_value_accuracy():
    output_file = '/home/user/center_value.txt'

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        val_str = f.read().strip()

    try:
        agent_val = float(val_str)
    except ValueError:
        assert False, f"Could not parse the contents of {output_file} as a float. Found: {val_str}"

    # Analytical solution at center (x=1.0, y=0.5):
    # u(1.0, 0.5) = sin(pi/2) * sinh(pi/4) / sinh(pi/2)
    target_val = math.sin(math.pi / 2.0) * math.sinh(math.pi / 4.0) / math.sinh(math.pi / 2.0)

    error = abs(agent_val - target_val)
    threshold = 0.01

    assert error < threshold, (
        f"Agent's computed center value {agent_val} is too far from the analytical "
        f"target {target_val:.5f}. Absolute error: {error:.5f} >= threshold {threshold}"
    )