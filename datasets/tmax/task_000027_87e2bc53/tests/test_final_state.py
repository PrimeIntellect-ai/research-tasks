# test_final_state.py

import os
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Test that the required scripts exist and have execute permissions."""
    setup_script = "/home/user/setup_index.sh"
    query_script = "/home/user/query_traversal.sh"

    assert os.path.exists(setup_script), f"Script {setup_script} is missing."
    assert os.path.isfile(setup_script), f"Path {setup_script} is not a file."
    assert os.access(setup_script, os.X_OK), f"Script {setup_script} is not executable."

    assert os.path.exists(query_script), f"Script {query_script} is missing."
    assert os.path.isfile(query_script), f"Path {query_script} is not a file."
    assert os.access(query_script, os.X_OK), f"Script {query_script} is not executable."

def test_setup_index_execution_and_output():
    """Test that setup_index.sh creates the correct index files."""
    setup_script = "/home/user/setup_index.sh"
    index_dir = "/home/user/graph_index"

    # Run the setup script
    result = subprocess.run([setup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"setup_index.sh failed with return code {result.returncode}. stderr: {result.stderr}"

    assert os.path.exists(index_dir), f"Directory {index_dir} was not created."
    assert os.path.isdir(index_dir), f"Path {index_dir} is not a directory."

    # Check content of A.txt
    a_txt_path = os.path.join(index_dir, "A.txt")
    assert os.path.exists(a_txt_path), f"File {a_txt_path} was not created."

    with open(a_txt_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = ["B", "C", "D", "I"]
    assert content == expected_content, f"Content of {a_txt_path} is incorrect. Expected {expected_content}, got {content}."

def test_query_traversal_execution_and_output():
    """Test that query_traversal.sh produces the correct output for node A."""
    query_script = "/home/user/query_traversal.sh"

    # Run the query script
    result = subprocess.run([query_script, "A"], capture_output=True, text=True)
    assert result.returncode == 0, f"query_traversal.sh failed with return code {result.returncode}. stderr: {result.stderr}"

    output_lines = result.stdout.strip().splitlines()
    expected_lines = [
        "E,4",
        "F,2",
        "J,1"
    ]

    assert output_lines == expected_lines, f"Output of query_traversal.sh is incorrect. Expected {expected_lines}, got {output_lines}."