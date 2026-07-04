# test_final_state.py
import os
import pytest

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"The flag file was not found at {flag_path}"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_n0n3_alg_m4ster_rust_8812}"
    assert content == expected_flag, f"The flag file content is incorrect. Expected {expected_flag}, got {content}"

def test_rust_project_exists():
    project_dir = "/home/user/exploit_project"
    assert os.path.isdir(project_dir), f"The Rust project directory was not found at {project_dir}"

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml is missing in {project_dir}"

    main_rs = os.path.join(project_dir, "src", "main.rs")
    assert os.path.isfile(main_rs), f"src/main.rs is missing in {project_dir}"