# test_final_state.py
import os

def test_fit_result_exists_and_correct():
    """Test that the fit result file exists and contains the correct m,c values."""
    result_file = '/home/user/fit_result.txt'
    assert os.path.isfile(result_file), f"Expected result file {result_file} does not exist."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    expected = "2.0000,0.0600"
    assert content == expected, f"File content '{content}' does not match expected '{expected}'."

def test_rust_project_exists():
    """Test that the Rust project was created in the correct directory and uses the hdf5 crate."""
    project_dir = '/home/user/fit_model'
    cargo_toml = os.path.join(project_dir, 'Cargo.toml')

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}."

    with open(cargo_toml, 'r') as f:
        content = f.read()

    assert 'hdf5' in content, "The 'hdf5' crate is not listed as a dependency in Cargo.toml."