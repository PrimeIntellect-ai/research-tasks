# test_final_state.py
import os

def test_rust_code_modified():
    main_rs_path = "/home/user/data_gen/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist"
    with open(main_rs_path, "r") as f:
        content = f.read()
        # Verify the student removed the non-deterministic Mutex approach
        assert "Mutex::new" not in content, "main.rs still contains Mutex::new usage which causes non-determinism"
        assert "par_iter" not in content, "main.rs still contains par_iter usage for the reduction"
        assert "iter()" in content, "main.rs should use sequential iter()"
        assert "sum()" in content or "sum::<" in content, "main.rs should use sum() for reduction"

def test_binary_compiled():
    binary_path = "/home/user/data_gen/target/release/data_gen"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}. Did you run 'cargo build --release'?"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_output_features_matches_reference():
    output_path = "/home/user/output_features.csv"
    reference_path = "/home/user/reference_features.csv"

    assert os.path.isfile(output_path), f"{output_path} does not exist. Did you run the compiled binary?"
    assert os.path.isfile(reference_path), f"{reference_path} is missing."

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    with open(reference_path, "r") as f:
        reference_content = f.read().strip()

    assert output_content == reference_content, f"Output features ({output_content}) do not exactly match reference features ({reference_content})."

def test_regression_result_file():
    result_path = "/home/user/regression_result.txt"
    reference_path = "/home/user/reference_features.csv"

    assert os.path.isfile(result_path), f"{result_path} does not exist."
    assert os.path.isfile(reference_path), f"{reference_path} is missing."

    with open(reference_path, "r") as f:
        reference_content = f.read().strip()

    with open(result_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"{result_path} must contain at least 2 lines."
    assert lines[0] == "PASS", f"First line of {result_path} must be exactly 'PASS', got '{lines[0]}'."
    assert lines[1] == reference_content, f"Second line of {result_path} must exactly match the reference output '{reference_content}', got '{lines[1]}'."