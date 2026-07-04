# test_final_state.py
import os
import json
import math
import pytest

def test_results_json_exists():
    assert os.path.isfile("/app/results.json"), "/app/results.json does not exist."

def test_results_json_structure():
    with open("/app/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/app/results.json is not a valid JSON file.")

    assert "k_deg" in data, "Missing 'k_deg' in results.json"
    assert "mu" in data, "Missing 'mu' in results.json"
    assert "sigma" in data, "Missing 'sigma' in results.json"
    assert "concentrations" in data, "Missing 'concentrations' in results.json"
    assert isinstance(data["concentrations"], dict), "'concentrations' must be a dictionary"
    assert len(data["concentrations"]) == 100, f"Expected 100 concentrations, got {len(data['concentrations'])}"

def test_mae_metric_threshold():
    with open("/app/results.json", "r") as f:
        data = json.load(f)

    k_deg_true = 0.284

    # Read FASTA to get true GC contents
    gc_contents = {}
    with open('/app/sequences.fasta', 'r') as f:
        seq_id = ""
        seq_data = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    gc_contents[seq_id] = (seq_data.count('G') + seq_data.count('C')) / len(seq_data)
                seq_id = line[1:]
                seq_data = ""
            else:
                seq_data += line
        if seq_id:
            gc_contents[seq_id] = (seq_data.count('G') + seq_data.count('C')) / len(seq_data)

    errors = []
    agent_concs = data.get("concentrations", {})

    for sid, gc in gc_contents.items():
        assert sid in agent_concs, f"Missing sequence {sid} in concentrations"

        k_syn = 5.0 * gc
        # Analytical solution
        true_P = (k_syn / k_deg_true) * (1 - math.exp(-k_deg_true * 100.0))
        agent_P = float(agent_concs[sid])
        errors.append(abs(true_P - agent_P))

    mae = sum(errors) / len(errors)

    assert mae <= 0.05, f"MAE is {mae}, which is higher than the allowed threshold of 0.05"