# test_final_state.py

import json
import os
import pytest

def test_audit_trail_jaccard_similarity():
    """Verify the audit trail JSON exists, is valid, and matches the expected configurations."""
    audit_file = "/home/user/audit_trail.json"

    assert os.path.isfile(audit_file), f"Audit trail file is missing at {audit_file}"

    try:
        with open(audit_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {audit_file} is not valid JSON.")

    assert isinstance(data, dict), f"JSON root must be an object/dict, got {type(data).__name__}"

    agent_ssh = data.get("active_ssh_ciphers", [])
    agent_tls = data.get("active_tls_versions", [])

    assert isinstance(agent_ssh, list), "active_ssh_ciphers must be a list"
    assert isinstance(agent_tls, list), "active_tls_versions must be a list"

    agent_list = set([str(c).lower().strip() for c in agent_ssh] + 
                     [str(t).lower().strip() for t in agent_tls])

    ground_truth = {"aes128-cbc", "3des-cbc", "tlsv1.1"}

    intersection = len(agent_list.intersection(ground_truth))
    union = len(agent_list.union(ground_truth))

    if union == 0:
        jaccard = 0.0
    else:
        jaccard = intersection / union

    assert jaccard >= 0.85, (
        f"Jaccard similarity {jaccard:.4f} is below threshold 0.85. "
        f"Agent found: {agent_list}, Expected: {ground_truth}"
    )