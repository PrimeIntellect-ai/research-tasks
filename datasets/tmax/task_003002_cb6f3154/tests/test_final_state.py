# test_final_state.py

import os
import stat
import math

def test_training_label_correct():
    """Test that the training label is correctly computed and reproducible."""
    label_path = "/home/user/training_label.txt"
    assert os.path.isfile(label_path), f"File {label_path} does not exist. Did you run the script?"

    with open(label_path, "r") as f:
        content = f.read().strip()

    # Recompute the expected value to ensure exact correctness
    # sin(i)*10 + 20 scaled by 0.987
    values = []
    for i in range(1, 101):
        val = (math.sin(i) * 10 + 20) * 0.987
        values.append(val)

    values.sort()

    expected_dist = 0.0
    for nr, val in enumerate(values, start=1):
        expected_dist += (val - (nr * 0.5)) ** 2

    expected_str = f"{expected_dist:.6f}"

    assert content == expected_str, f"Expected training_label.txt to contain {expected_str}, but found {content}."

def test_script_modifications():
    """Test that the script was modified correctly to include sorting and keep parallelization."""
    script_path = "/home/user/build_dataset.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is no longer executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "xargs" in content and "-P" in content, "Parallel extraction logic (xargs -P) was removed or altered."
    assert "sort" in content, "The script does not seem to contain 'sort' to order the values."
    assert "awk" in content and "dist +=" in content, "The awk calculation logic was removed or altered."