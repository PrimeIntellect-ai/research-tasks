# test_final_state.py

import os
import math

def test_anomalies_txt_exists_and_correct():
    path = "/home/user/anomalies.txt"
    assert os.path.exists(path), f"File {path} is missing. The script did not generate it."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, but found {len(lines)}."

    # Expected calculations (can be recomputed or directly checked since the input is fixed)
    # s5: (1 - exp(-3.50)) * 0.9 = 0.872822
    # s3: (1 - exp(-2.99)) * 0.7 = 0.664815
    # s6: (1 - exp(-1.20)) * 0.95 = 0.663865

    expected = [
        ("s5", 0.872822),
        ("s3", 0.664815),
        ("s6", 0.663865)
    ]

    for i, (line, (exp_sensor, exp_prob)) in enumerate(zip(lines, expected)):
        parts = line.split()
        assert len(parts) == 2, f"Line {i+1} is malformed: '{line}'. Expected format 'sensor_id probability'."

        sensor, prob_str = parts
        assert sensor == exp_sensor, f"Line {i+1}: expected sensor '{exp_sensor}', got '{sensor}'."

        try:
            prob = float(prob_str)
        except ValueError:
            assert False, f"Line {i+1}: probability '{prob_str}' is not a valid float."

        assert math.isclose(prob, exp_prob, abs_tol=1e-5), \
            f"Line {i+1}: expected probability ~{exp_prob:.6f}, got {prob:.6f}."