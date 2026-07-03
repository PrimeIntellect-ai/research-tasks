# test_final_state.py

import os
import stat

def test_dataset_csv_content():
    """Check that dataset.csv exists and has the exact expected content."""
    csv_path = "/home/user/dataset.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    expected_content = (
        "f,max_error,peak_freq\n"
        "1,0.2222,1.0\n"
        "2,3.3130,2.0\n"
        "3,31.0664,3.0\n"
        "4,250.7850,4.0\n"
        "5,1730.0175,5.0\n"
    )

    with open(csv_path, "r") as f:
        content = f.read()

    # Strip trailing whitespace/newlines for a robust comparison
    assert content.strip() == expected_content.strip(), f"Content of {csv_path} does not match expected output."

def test_scripts_exist_and_permissions():
    """Check that the scripts exist and the bash script is executable."""
    bash_script = "/home/user/build_dataset.sh"
    py_script = "/home/user/generate_features.py"

    assert os.path.exists(bash_script), f"Bash script {bash_script} does not exist."
    assert os.path.exists(py_script), f"Python script {py_script} does not exist."

    st = os.stat(bash_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {bash_script} is not executable."