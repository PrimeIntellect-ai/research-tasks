# test_final_state.py

import os
import json
import math

def test_script_exists():
    """Check that the prepare_data.py script exists."""
    script_path = "/home/user/prepare_data.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_output_json_exists_and_correct():
    """Check that training_data.json exists and contains the correct values."""
    output_path = "/home/user/training_data.json"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {output_path} does not contain valid JSON."

    # Check structure
    assert "local_minimum" in data, "Key 'local_minimum' missing in JSON."
    assert "segments_power" in data, "Key 'segments_power' missing in JSON."

    local_min = data["local_minimum"]
    assert "t" in local_min, "Key 't' missing in 'local_minimum'."
    assert "f_t" in local_min, "Key 'f_t' missing in 'local_minimum'."

    segments = data["segments_power"]
    assert isinstance(segments, list), "'segments_power' must be a list."
    assert len(segments) == 4, "'segments_power' must contain exactly 4 segments."

    # Verify values with a small tolerance due to rounding
    expected_t = 8.1678
    expected_f_t = -4.0156
    expected_power = 600.6726

    assert math.isclose(local_min["t"], expected_t, abs_tol=0.001), \
        f"Expected local_minimum.t to be near {expected_t}, got {local_min['t']}."

    assert math.isclose(local_min["f_t"], expected_f_t, abs_tol=0.001), \
        f"Expected local_minimum.f_t to be near {expected_f_t}, got {local_min['f_t']}."

    for i, seg in enumerate(segments):
        assert "segment" in seg, f"Key 'segment' missing in segments_power[{i}]."
        assert "power" in seg, f"Key 'power' missing in segments_power[{i}]."
        assert seg["segment"] == i, f"Expected segment index {i}, got {seg['segment']}."
        assert math.isclose(seg["power"], expected_power, abs_tol=0.001), \
            f"Expected power for segment {i} to be near {expected_power}, got {seg['power']}."