# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/grpc_refactor_pr"

def test_workflow_fixed():
    """Verify the GitHub Actions workflow file has the corrected commands."""
    workflow_path = os.path.join(BASE_DIR, ".github", "workflows", "rust.yml")
    assert os.path.isfile(workflow_path), f"Missing github workflow at {workflow_path}"

    with open(workflow_path, "r") as f:
        content = f.read()

    assert "cargo fmt --check" in content, "Workflow missing corrected 'cargo fmt --check' command"
    assert "cargo test" in content, "Workflow missing corrected 'cargo test' command"
    assert "cargo build --release" in content, "Workflow missing corrected 'cargo build --release' command"

    assert "cargo fmt --chek" not in content, "Workflow still contains broken 'cargo fmt --chek'"
    assert "cargo tesst" not in content, "Workflow still contains broken 'cargo tesst'"
    assert "cargo buid" not in content, "Workflow still contains broken 'cargo buid'"

def test_common_crate_exists():
    """Verify that the common crate was created."""
    common_cargo_path = os.path.join(BASE_DIR, "common", "Cargo.toml")
    assert os.path.isfile(common_cargo_path), f"Missing common crate Cargo.toml at {common_cargo_path}"

def test_dependencies_fixed():
    """Verify that the circular dependency is resolved and both depend on common."""
    client_cargo = os.path.join(BASE_DIR, "client", "Cargo.toml")
    server_cargo = os.path.join(BASE_DIR, "server", "Cargo.toml")

    assert os.path.isfile(client_cargo), f"Missing client Cargo.toml at {client_cargo}"
    assert os.path.isfile(server_cargo), f"Missing server Cargo.toml at {server_cargo}"

    with open(client_cargo, "r") as f:
        client_content = f.read()

    with open(server_cargo, "r") as f:
        server_content = f.read()

    # Check client dependencies
    assert "server =" not in client_content and "server=" not in client_content, \
        "Client still depends on server"
    assert "common" in client_content, "Client does not depend on common crate"

    # Check server dependencies
    assert "client =" not in server_content and "client=" not in server_content, \
        "Server still depends on client"
    assert "common" in server_content, "Server does not depend on common crate"

def test_verification_log():
    """Verify the client successfully parsed the JSON, called the server, and logged the output."""
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Missing verification log at {log_path}. Did you run the client and save the output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_output = "RESPONSE=Processed secret_data_99 with config retries 3"
    assert expected_output in content, f"Verification log does not contain the expected output. Found: {content}"