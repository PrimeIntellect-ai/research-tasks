# test_final_state.py
import os
import pytest

def test_dos2unix_compiled():
    """Check if dos2unix was successfully compiled."""
    binary_path = "/app/dos2unix-7.4.3/dos2unix"
    assert os.path.exists(binary_path), f"dos2unix binary not found at {binary_path}. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"dos2unix binary at {binary_path} is not executable."

def test_pipeline_script_exists():
    """Check if the pipeline script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script not found at {script_path}."
    assert os.access(script_path, os.X_OK) or os.path.getsize(script_path) > 0, f"Pipeline script at {script_path} is empty."

def test_pipeline_log_exists():
    """Check if the pipeline log exists and contains log entries."""
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Pipeline log not found at {log_path}."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"Pipeline log at {log_path} is empty."
    assert "Started processing" in content or "Completed dos2unix" in content or "]" in content, "Pipeline log does not contain expected log entries."

def test_normalized_subs_metric():
    """Calculate Exact Line Match Ratio and assert it is >= 0.90."""
    agent_output_path = "/home/user/normalized_subs.tsv"
    golden_reference_path = "/golden/reference.tsv"

    assert os.path.exists(agent_output_path), f"Agent output file not found at {agent_output_path}."
    assert os.path.exists(golden_reference_path), f"Golden reference file not found at {golden_reference_path}."

    with open(agent_output_path, "r", encoding="utf-8") as f:
        agent_lines = [line.strip() for line in f if line.strip()]

    with open(golden_reference_path, "r", encoding="utf-8") as f:
        golden_lines = [line.strip() for line in f if line.strip()]

    assert len(golden_lines) > 0, "Golden reference is empty."

    agent_set = set(agent_lines)
    golden_set = set(golden_lines)

    match_ratio = len(agent_set & golden_set) / len(golden_set)

    assert match_ratio >= 0.90, f"Exact Line Match Ratio is {match_ratio:.4f}, which is below the threshold of 0.90."