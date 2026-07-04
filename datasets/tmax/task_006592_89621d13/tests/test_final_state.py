# test_final_state.py

import os
import re

def test_slopes_file_exists():
    assert os.path.exists("/home/user/slopes.txt"), "The file /home/user/slopes.txt does not exist."

def test_slopes_content():
    with open("/home/user/slopes.txt", "r") as f:
        content = f.read()

    # Parse slope for ID 0
    m0 = re.search(r"^0:\s*([0-9\.]+)", content, re.MULTILINE)
    assert m0 is not None, "Could not find slope for ID 0 in slopes.txt. Ensure the format is '0: <slope>'"
    val0 = float(m0.group(1))
    assert abs(val0 - 2.0) < 1e-5, f"Expected slope for ID 0 to be 2.0, but got {val0}. The NaN records might not be properly skipped."

    # Parse slope for ID 1
    m1 = re.search(r"^1:\s*([0-9\.]+)", content, re.MULTILINE)
    assert m1 is not None, "Could not find slope for ID 1 in slopes.txt. Ensure the format is '1: <slope>'"
    val1 = float(m1.group(1))
    assert abs(val1 - 3.5) < 1e-5, f"Expected slope for ID 1 to be 3.5, but got {val1}."