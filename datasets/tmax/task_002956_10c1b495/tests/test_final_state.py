# test_final_state.py
import os

def test_cleaned_measurements_exists():
    file_path = "/home/user/cleaned_measurements.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_cleaned_measurements_content():
    file_path = "/home/user/cleaned_measurements.csv"
    expected_content = """id,measurement,value
X-1,p1,10.5
X-1,p2,12.5
X-1,p4,14.2
X-2,p1,11.1
X-3,p5,5.5
Y-9,m1,-2.0
Y-9,m2,0.0"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content.strip(), f"Content of {file_path} does not match the expected output."

def test_rust_project_exists():
    project_dir = "/home/user/cleaner"
    cargo_toml_path = os.path.join(project_dir, "Cargo.toml")

    assert os.path.exists(project_dir), f"Rust project directory {project_dir} is missing."
    assert os.path.isdir(project_dir), f"{project_dir} should be a directory."
    assert os.path.exists(cargo_toml_path), f"Cargo.toml is missing in {project_dir}."

def test_rust_project_uses_rayon():
    cargo_toml_path = "/home/user/cleaner/Cargo.toml"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    assert "rayon" in content, "The 'rayon' crate is not listed in Cargo.toml."