# test_final_state.py
import os
import re

def test_final_population_file_exists():
    assert os.path.isfile("/home/user/final_population.txt"), "/home/user/final_population.txt is missing"

def test_final_population_values():
    with open("/home/user/final_population.txt", "r") as f:
        content = f.read().strip()

    try:
        vals = [float(x.strip()) for x in content.split(',')]
    except ValueError:
        assert False, "Could not parse the contents of /home/user/final_population.txt as a comma-separated list of floats"

    assert len(vals) == 3, f"Expected 3 values in final_population.txt, found {len(vals)}"

    expected = [16.89, 25.69, 8.51]

    for i, (v, e) in enumerate(zip(vals, expected)):
        assert abs(v - e) <= 0.1, f"Value at index {i} ({v}) deviates too much from expected ({e})"

def test_main_rs_fixed():
    main_rs_path = "/home/user/seq_model/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check if the logic is fixed. 
    # Original: if error > tol { dt *= 1.2; } else { state = corrector; t += dt; dt *= 0.5; }
    # Fixed: if error > tol { dt *= 0.5; } else { state = corrector; t += dt; dt *= 1.2; }

    # We can just verify the file compiles and runs to the correct output, but it's good to check the source roughly.
    # The output check is the strongest assertion.
    assert "error > tol" in content, "Error tolerance check not found in main.rs"