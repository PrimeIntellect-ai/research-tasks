# test_final_state.py
import os

def test_final_output_exists():
    """Check if final_output.txt was created."""
    output_path = "/home/user/repro_eval/final_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_final_output_content():
    """Check if the final output contains the correct deterministic value."""
    output_path = "/home/user/repro_eval/final_output.txt"
    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_value = "-0.932909477028741"
    assert content == expected_value, f"Expected output {expected_value}, but got {content}. Floating point reduction order is likely still incorrect or non-deterministic."

def test_main_rs_modified_for_determinism():
    """Check if src/main.rs was modified to use a deterministic approach."""
    main_rs_path = "/home/user/repro_eval/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # The fix should involve either BTreeMap or sorting the keys/entries
    has_btree = "BTreeMap" in content
    has_sort = "sort" in content

    assert has_btree or has_sort, "src/main.rs does not appear to use BTreeMap or sorting, which is required to fix the non-deterministic reduction order."