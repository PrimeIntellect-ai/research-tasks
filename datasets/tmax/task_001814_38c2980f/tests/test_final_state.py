# test_final_state.py

import os
import json
import pytest

def test_binaries_exist():
    analyzer_path = "/home/user/bin/analyzer"
    extractor_path = "/home/user/bin/extractor"

    assert os.path.isfile(analyzer_path), f"Go analyzer binary not found at {analyzer_path}"
    assert os.access(analyzer_path, os.X_OK), f"Go analyzer binary at {analyzer_path} is not executable"

    assert os.path.isfile(extractor_path), f"C++ extractor binary not found at {extractor_path}"
    assert os.access(extractor_path, os.X_OK), f"C++ extractor binary at {extractor_path} is not executable"

def test_organized_assets():
    organized_dir = "/home/user/videoproc/organized_assets"
    assert os.path.isdir(organized_dir), f"Organized assets directory not found at {organized_dir}"

    # Check that it's not empty
    files = []
    for root, _, filenames in os.walk(organized_dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    assert len(files) > 0, f"Organized assets directory {organized_dir} is empty"

def test_pipeline_script():
    pipeline_path = "/home/user/videoproc/pipeline.py"
    assert os.path.isfile(pipeline_path), f"Python pipeline script not found at {pipeline_path}"

def test_output_metrics_mse():
    agent_file = "/home/user/output_metrics.json"
    reference_file = "/tmp/ground_truth_metrics.json"

    assert os.path.isfile(agent_file), f"Output metrics file not found at {agent_file}"
    assert os.path.isfile(reference_file), f"Reference metrics file not found at {reference_file}"

    with open(agent_file, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse JSON from {agent_file}")

    with open(reference_file, 'r') as f:
        ref_data = json.load(f)

    assert isinstance(agent_data, list), f"Expected JSON array in {agent_file}"
    assert len(agent_data) == len(ref_data), f"Length mismatch: agent has {len(agent_data)}, reference has {len(ref_data)}"

    mse = sum((a - r) ** 2 for a, r in zip(agent_data, ref_data)) / len(ref_data)

    assert mse <= 1.5, f"MSE {mse} exceeds threshold of 1.5"