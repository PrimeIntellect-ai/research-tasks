# test_final_state.py

import os
import json

def test_dashboard_json_exists_and_correct():
    json_path = "/home/user/dashboard.json"

    assert os.path.exists(json_path), f"Expected file {json_path} does not exist."
    assert os.path.isfile(json_path), f"Expected {json_path} to be a file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    assert "panels" in data, "JSON missing 'panels' key."
    assert isinstance(data["panels"], list), "'panels' must be a list."
    assert len(data["panels"]) > 0, "'panels' list is empty."

    panel = data["panels"][0]
    assert panel.get("title") == "tun0 Traffic", "Panel title is not 'tun0 Traffic'."

    assert "metrics" in panel, "Panel missing 'metrics' key."
    metrics = panel["metrics"]

    assert metrics.get("rx_bytes") == 154321, f"Expected rx_bytes to be 154321, got {metrics.get('rx_bytes')}."
    assert metrics.get("tx_bytes") == 89432, f"Expected tx_bytes to be 89432, got {metrics.get('tx_bytes')}."
    assert metrics.get("drops") == 12, f"Expected drops to be 12, got {metrics.get('drops')}."