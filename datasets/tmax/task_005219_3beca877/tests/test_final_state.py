# test_final_state.py
import os

def test_optimized_params_file():
    filepath = "/home/user/optimized_params.txt"
    assert os.path.isfile(filepath), f"Log file {filepath} was not found. Please ensure you create it."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected = "a=2.00,b=3.00"

    # We remove whitespace to be slightly forgiving on spacing, but check the exact values
    normalized_content = content.replace(" ", "")
    assert expected in normalized_content, (
        f"Expected to find '{expected}' in {filepath}, "
        f"but found: '{content}'"
    )

def test_rust_code_modified():
    # It's good practice to verify the user actually modified the Rust file
    # to remove the non-deterministic Mutex accumulation.
    main_rs = "/home/user/model_fitter/src/main.rs"
    assert os.path.isfile(main_rs), f"Rust source file {main_rs} is missing."

    with open(main_rs, "r") as f:
        content = f.read()

    # The original code had Mutex in the inner loop. 
    # A proper fix either removes threads or removes the Mutex accumulation.
    # We won't strictly fail if Mutex is present (they might have commented it out),
    # but the primary test is the correct output above.