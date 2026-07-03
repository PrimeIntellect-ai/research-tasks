# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/staged_rollout.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_frontend_canary_output():
    output_path = "/home/user/deploy_out/frontend_canary.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} is not valid JSON.")

    # Check replicas
    replicas = data.get("spec", {}).get("replicas")
    assert replicas == 1, f"Expected replicas to be 1 in {output_path}, but got {replicas}."

    # Check image
    try:
        image = data["spec"]["template"]["spec"]["containers"][0]["image"]
    except KeyError:
        pytest.fail(f"The file {output_path} does not have the expected container image structure.")

    expected_image = "registry.local/frontend:2.0-canary"
    assert image == expected_image, f"Expected image to be '{expected_image}' in {output_path}, but got '{image}'."

def test_backend_production_output():
    output_path = "/home/user/deploy_out/backend_production.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} is not valid JSON.")

    # Check replicas
    replicas = data.get("spec", {}).get("replicas")
    assert replicas == 5, f"Expected replicas to be 5 in {output_path}, but got {replicas}."

    # Check image
    try:
        image = data["spec"]["template"]["spec"]["containers"][0]["image"]
    except KeyError:
        pytest.fail(f"The file {output_path} does not have the expected container image structure.")

    expected_image = "registry.local/backend:1.5"
    assert image == expected_image, f"Expected image to be '{expected_image}' in {output_path}, but got '{image}'."

def test_json_indentation():
    # Check that the files were saved with 2 spaces indentation
    for output_path in [
        "/home/user/deploy_out/frontend_canary.json",
        "/home/user/deploy_out/backend_production.json"
    ]:
        if os.path.isfile(output_path):
            with open(output_path, 'r') as f:
                lines = f.readlines()
                # Find the first indented line (usually line 2)
                if len(lines) > 1:
                    second_line = lines[1]
                    # Count leading spaces
                    leading_spaces = len(second_line) - len(second_line.lstrip(' '))
                    assert leading_spaces == 2, f"Expected 2 spaces indentation in {output_path}, but found {leading_spaces} spaces."