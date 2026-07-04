# test_final_state.py

import os
import json
import subprocess
import pytest

def test_script_exists():
    """Verify that the user created the automation script."""
    assert os.path.isfile("/home/user/automate_container.py"), "The script /home/user/automate_container.py does not exist."

def test_script_execution_and_output():
    """Run the script and verify the resulting output file."""
    # Run the agent's script
    result = subprocess.run(
        ["python3", "/home/user/automate_container.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"

    output_file = "/home/user/routes_output.json"
    assert os.path.exists(output_file), f"The expected output file {output_file} was not created."

    with open(output_file, 'r') as f:
        try:
            routes = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_file} does not contain valid JSON.")

    assert isinstance(routes, list), f"The JSON in {output_file} should be a list of routes."

    # Verify the specific route
    found_route = False
    for route in routes:
        if route.get('dst') == '192.168.100.0/24' and route.get('dev') == 'net0':
            found_route = True
            break

    assert found_route, "The correct route for 192.168.100.0/24 on net0 was not found in the output JSON."