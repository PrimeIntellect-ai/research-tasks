# test_final_state.py

import os
import json

def test_team_summary_exists():
    filepath = "/home/user/team_summary.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

def test_team_summary_content():
    filepath = "/home/user/team_summary.json"
    assert os.path.isfile(filepath), f"Expected output file {filepath} is missing."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{filepath} does not contain valid JSON."

    expected_data = {
        "TeamAlpha": {
            "total_endpoints": 3,
            "outbound_dependencies": 1
        },
        "TeamBeta": {
            "total_endpoints": 5,
            "outbound_dependencies": 4
        },
        "TeamGamma": {
            "total_endpoints": 2,
            "outbound_dependencies": 2
        }
    }

    assert isinstance(data, dict), f"Expected a JSON object at the root of {filepath}."

    for team, expected_metrics in expected_data.items():
        assert team in data, f"Missing team '{team}' in {filepath}."
        metrics = data[team]
        assert "total_endpoints" in metrics, f"Missing 'total_endpoints' for team '{team}'."
        assert "outbound_dependencies" in metrics, f"Missing 'outbound_dependencies' for team '{team}'."

        assert metrics["total_endpoints"] == expected_metrics["total_endpoints"], \
            f"Incorrect total_endpoints for '{team}'. Expected {expected_metrics['total_endpoints']}, got {metrics['total_endpoints']}."
        assert metrics["outbound_dependencies"] == expected_metrics["outbound_dependencies"], \
            f"Incorrect outbound_dependencies for '{team}'. Expected {expected_metrics['outbound_dependencies']}, got {metrics['outbound_dependencies']}."

    # Check for extra unexpected teams
    for team in data.keys():
        assert team in expected_data, f"Unexpected team '{team}' found in {filepath}."