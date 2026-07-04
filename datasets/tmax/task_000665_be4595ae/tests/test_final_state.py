# test_final_state.py
import os
import re
import math

def test_sim_c_exists():
    """Verify that the C source file was created."""
    assert os.path.isfile("/home/user/sim.c"), "/home/user/sim.c does not exist."

def test_result_txt_exists():
    """Verify that the result.txt file was created."""
    assert os.path.isfile("/home/user/result.txt"), "/home/user/result.txt does not exist."

def test_result_values():
    """Parse result.txt and verify the computed values."""
    with open("/home/user/result.txt", "r") as f:
        content = f.read()

    score_match = re.search(r"Score:\s*(-?\d+)", content)
    mass_match = re.search(r"Total Mass:\s*(-?\d+\.\d+)", content)
    kl_match = re.search(r"KL:\s*(-?\d+\.\d+)", content)

    assert score_match is not None, "Could not find 'Score: <integer>' in result.txt"
    assert mass_match is not None, "Could not find 'Total Mass: <float>' in result.txt"
    assert kl_match is not None, "Could not find 'KL: <float>' in result.txt"

    score = int(score_match.group(1))
    mass = float(mass_match.group(1))
    kl = float(kl_match.group(1))

    assert score == 7, f"Expected Score to be 7, but got {score}"
    assert math.isclose(mass, 17.726359, abs_tol=1e-4), f"Expected Total Mass ~17.726359, but got {mass}"
    assert math.isclose(kl, 0.811568, abs_tol=1e-4), f"Expected KL ~0.811568, but got {kl}"