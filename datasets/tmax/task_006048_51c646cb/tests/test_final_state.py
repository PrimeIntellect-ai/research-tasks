# test_final_state.py

import os

def test_vulnerable_servers_log():
    """Test that the vulnerable_servers.log contains the correct output."""
    log_path = '/home/user/vulnerable_servers.log'
    assert os.path.exists(log_path), f"Failure: Output file not found at {log_path}."

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["Server_Alpha", "Server_Delta", "Server_Gamma"]
    assert lines == expected, f"Failure: Expected {expected}, got {lines}"

def test_audit_script_exists_and_uses_rdflib():
    """Test that the python script exists and contains expected rdflib / query features."""
    script_path = '/home/user/audit_vulnerabilities.py'
    assert os.path.exists(script_path), f"Failure: Script not found at {script_path}."

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'rdflib' in content, "Failure: The script must import and use the 'rdflib' library."

    # Check for parameterized query usage (initBindings or prepareQuery)
    has_parameterization = 'initBindings' in content or 'prepareQuery' in content
    assert has_parameterization, "Failure: The script must use parameterized queries (e.g., initBindings or prepareQuery)."

    # Check for graph matching features to filter out active patches
    has_graph_filtering = 'MINUS' in content.upper() or 'FILTER NOT EXISTS' in content.upper() or 'NOT EXISTS' in content.upper()
    assert has_graph_filtering, "Failure: The script's SPARQL query must use graph matching features like MINUS or FILTER NOT EXISTS."