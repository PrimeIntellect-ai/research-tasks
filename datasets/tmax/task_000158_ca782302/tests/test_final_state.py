# test_final_state.py

import os
import sys
import json
import time
import subprocess
import pytest

def test_audioproc_execution_and_performance():
    executable = "/home/user/audioproc/build/audioproc"
    input_wav = "/app/telemetry.wav"
    output_json = "/home/user/output.json"

    assert os.path.exists(executable), f"Executable not found at {executable}. Did you build it?"
    assert os.path.exists(input_wav), f"Input audio file not found at {input_wav}."

    # Remove output file if it exists to ensure we are testing the new run
    if os.path.exists(output_json):
        os.remove(output_json)

    start_time = time.time()
    proc = subprocess.run(
        [executable, input_wav, output_json],
        capture_output=True,
        text=True
    )
    end_time = time.time()

    exec_time = end_time - start_time

    assert proc.returncode == 0, f"audioproc failed with exit code {proc.returncode}. stderr: {proc.stderr}"
    assert exec_time <= 0.200, f"Execution time {exec_time:.4f}s exceeds the 0.200s threshold. Concurrency might not be implemented correctly or is too slow."

def test_audioproc_json_schema():
    output_json = "/home/user/output.json"
    assert os.path.exists(output_json), f"Output JSON file not found at {output_json}."

    with open(output_json, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse output JSON: {e}")

    assert "metadata" in data, "Key 'metadata' missing from JSON output."
    assert "source" in data["metadata"], "Key 'source' missing from 'metadata'."
    assert data["metadata"]["source"] == "/app/telemetry.wav", f"Expected metadata.source to be '/app/telemetry.wav', got {data['metadata']['source']}"

    assert "measurements" in data, "Key 'measurements' missing from JSON output."
    assert isinstance(data["measurements"], list), "'measurements' should be a list."
    assert len(data["measurements"]) > 0, "'measurements' list is empty."

    previous_index = -1
    for i, measurement in enumerate(data["measurements"]):
        assert "chunk_index" in measurement, f"'chunk_index' missing in measurement at index {i}."
        assert "rms_value" in measurement, f"'rms_value' missing in measurement at index {i}."

        chunk_index = measurement["chunk_index"]
        rms_value = measurement["rms_value"]

        assert isinstance(chunk_index, int), f"'chunk_index' must be an integer, got {type(chunk_index)}."
        assert isinstance(rms_value, (int, float)), f"'rms_value' must be a number, got {type(rms_value)}."

        assert chunk_index > previous_index, f"Measurements are not ordered by chunk_index. Found {chunk_index} after {previous_index}."
        previous_index = chunk_index