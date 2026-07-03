# test_final_state.py

import os
import pytest

def test_sum_txt_exists_and_correct():
    sum_file_path = "/home/user/sum.txt"
    assert os.path.isfile(sum_file_path), f"The file {sum_file_path} does not exist. Did you run your Rust program?"

    with open(sum_file_path, "r") as f:
        content = f.read().strip()

    expected_sum = "27021597764222989"
    assert content == expected_sum, f"The sum in {sum_file_path} is incorrect. Expected '{expected_sum}', but got '{content}'."

def test_rust_project_exists():
    project_dir = "/home/user/cleaner"
    assert os.path.isdir(project_dir), f"The Rust project directory {project_dir} does not exist."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    src_dir = os.path.join(project_dir, "src")
    main_rs = os.path.join(src_dir, "main.rs")

    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}. Did you initialize the Rust project correctly?"
    assert os.path.isdir(src_dir), f"src directory not found in {project_dir}."
    assert os.path.isfile(main_rs), f"main.rs not found in {src_dir}."