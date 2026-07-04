# test_final_state.py
import os
import subprocess
import pytest

def test_container_running():
    """Test if the research_graph Docker container is running."""
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=research_graph", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    assert "research_graph" in result.stdout, "Container 'research_graph' is not running."

def test_script_exists_and_executable():
    """Test if /home/user/get_dependencies.sh exists and is executable."""
    script_path = "/home/user/get_dependencies.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_uses_parameters():
    """Test if the script uses parameterization for the Neo4j query."""
    script_path = "/home/user/get_dependencies.sh"
    with open(script_path, "r") as f:
        content = f.read()
    # Check for signs of parameterization in the JSON payload
    assert "parameters" in content.lower() or "props" in content.lower() or "$1" in content, \
        "Script does not seem to use a parameterized query (missing 'parameters' in payload)."

def test_script_execution_and_output():
    """Test if running the script with 'P1' produces the correct output in /home/user/output.txt."""
    script_path = "/home/user/get_dependencies.sh"
    output_path = "/home/user/output.txt"

    # Remove output file if it exists to ensure we are testing the script's execution
    if os.path.exists(output_path):
        os.remove(output_path)

    result = subprocess.run([script_path, "P1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    assert os.path.exists(output_path), f"Output file {output_path} was not created."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["P2", "P3", "P4", "P5", "P6", "P8"]
    assert lines == expected, f"Output file content {lines} does not match expected {expected}."