# test_final_state.py

import os
import json
import pytest

def test_cargo_toml_updated():
    cargo_path = "/home/user/project/Cargo.toml"
    policy_path = "/home/user/project/policy.json"

    assert os.path.isfile(cargo_path), f"{cargo_path} does not exist."
    assert os.path.isfile(policy_path), f"{policy_path} does not exist."

    with open(policy_path, "r") as f:
        policy = json.load(f)

    with open(cargo_path, "r") as f:
        cargo_content = f.read()

    deps = policy.get("dependencies", {})
    for dep, version_policy in deps.items():
        # Extract the version string after '>='
        if version_policy.startswith(">="):
            target_version = version_policy[2:]
        else:
            target_version = version_policy

        expected_line_single_quotes = f"{dep} = '{target_version}'"
        expected_line_double_quotes = f'{dep} = "{target_version}"'

        # We allow either single or double quotes, and optional spaces
        # But a simple check for the version string associated with the dep is robust enough
        # We will check if the target version is in the file, and specifically near the dep name
        assert (expected_line_double_quotes in cargo_content) or (expected_line_single_quotes in cargo_content) or (f'"{target_version}"' in cargo_content and dep in cargo_content), \
            f"Cargo.toml does not contain the updated version {target_version} for dependency {dep}."

def test_data_json_migrated():
    schema_v1_path = "/home/user/project/schema_v1.json"
    data_path = "/home/user/project/data.json"

    assert os.path.isfile(schema_v1_path), f"{schema_v1_path} does not exist."
    assert os.path.isfile(data_path), f"{data_path} does not exist."

    with open(schema_v1_path, "r") as f:
        schema_v1 = json.load(f)

    expected_data = []
    for item in schema_v1:
        expected_data.append({
            "id": item["id"],
            "full_name": f"{item['first_name']} {item['last_name']}"
        })

    with open(data_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{data_path} is not a valid JSON file.")

    assert actual_data == expected_data, f"The contents of {data_path} do not match the expected migrated schema."

def test_ci_pipeline_sh():
    script_path = "/home/user/project/ci_pipeline.sh"

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.strip().split('\n') if line.strip()]

    assert lines[0] == "#!/bin/bash", f"{script_path} must start with #!/bin/bash"

    # Check for navigation to the project directory
    navigated = any("cd /home/user/project" in line for line in lines)
    assert navigated, f"{script_path} does not navigate to /home/user/project"

    # Check for cargo check command
    cargo_checked = any("cargo check" in line for line in lines)
    assert cargo_checked, f"{script_path} does not run 'cargo check'"