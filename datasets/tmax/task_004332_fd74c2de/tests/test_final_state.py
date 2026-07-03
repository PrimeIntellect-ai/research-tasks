# test_final_state.py

import os
import re
import pytest

def test_peak_time_metric():
    """Check if the peak time is within the acceptable threshold."""
    path = "/home/user/peak_time.txt"
    assert os.path.isfile(path), f"Expected file at {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        agent_value = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {path} as a float: '{content}'")

    reference_value = 12.500
    threshold = 0.05
    error = abs(agent_value - reference_value)

    assert error < threshold, f"Absolute error {error} is not less than threshold {threshold} (Agent value: {agent_value}, Reference: {reference_value})"

def test_deployment_yaml_updated():
    """Check if the deployment.yaml has been updated to replicas: 3."""
    path = "/home/user/manifests/deployment.yaml"
    assert os.path.isfile(path), f"Expected file at {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "replicas: 3" in content, f"File {path} does not contain 'replicas: 3' as expected. Content:\n{content}"
    assert "replicas: 1" not in content, f"File {path} still contains 'replicas: 1'."

def test_operator_fstab_conf():
    """Check if the fstab config file contains the correct bind mount entry."""
    path = "/home/user/operator_fstab.conf"
    assert os.path.isfile(path), f"Expected file at {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    # The requirement says:
    # /home/user/manifests /var/lib/k8s/active_manifests none bind,ro 0 0
    # We should allow multiple spaces/tabs between fields.
    fields = content.split()
    assert len(fields) == 6, f"Expected 6 fields in fstab entry, found {len(fields)}: '{content}'"

    assert fields[0] == "/home/user/manifests", f"Expected first field to be '/home/user/manifests', got '{fields[0]}'"
    assert fields[1] == "/var/lib/k8s/active_manifests", f"Expected second field to be '/var/lib/k8s/active_manifests', got '{fields[1]}'"
    assert fields[2] == "none", f"Expected third field to be 'none', got '{fields[2]}'"

    # Options can be 'bind,ro' or 'ro,bind'
    opts = fields[3].split(',')
    assert set(opts) == {"bind", "ro"}, f"Expected options to be 'bind,ro', got '{fields[3]}'"

    assert fields[4] == "0", f"Expected fifth field to be '0', got '{fields[4]}'"
    assert fields[5] == "0", f"Expected sixth field to be '0', got '{fields[5]}'"