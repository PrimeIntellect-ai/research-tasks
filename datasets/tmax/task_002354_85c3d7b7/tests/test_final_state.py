# test_final_state.py

import os
import json
import base64
import math
import pytest

def get_expected(cpu, memory, uptime):
    score = (cpu * 1.5) + (memory * 2.0) / math.log(uptime + 2)
    checksum = math.sin(score) + math.cos(score)
    return score, checksum

def test_output_file_exists_and_correct():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"File {output_path} was not generated."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {output_path}, found {len(lines)}."

    expected_inputs = [
        {"id": "srv-1", "cpu": 50.0, "memory": 60.0, "uptime": 10},
        {"id": "srv-2", "cpu": 80.0, "memory": 90.0, "uptime": 5}
    ]

    for i, line in enumerate(lines):
        try:
            decoded_bytes = base64.b64decode(line)
            decoded_str = decoded_bytes.decode('utf-8')
            data = json.loads(decoded_str)
        except Exception as e:
            pytest.fail(f"Failed to decode and parse line {i+1} as base64-encoded JSON: {e}")

        expected_input = expected_inputs[i]
        assert data.get("server") == expected_input["id"], f"Expected server id {expected_input['id']} in line {i+1}."

        expected_score, expected_checksum = get_expected(
            expected_input["cpu"],
            expected_input["memory"],
            expected_input["uptime"]
        )

        assert "score" in data, f"'score' missing in line {i+1} JSON."
        assert "checksum" in data, f"'checksum' missing in line {i+1} JSON."

        assert math.isclose(data["score"], expected_score, rel_tol=1e-5), \
            f"Score for {expected_input['id']} is {data['score']}, expected {expected_score}."

        assert math.isclose(data["checksum"], expected_checksum, rel_tol=1e-5), \
            f"Checksum for {expected_input['id']} is {data['checksum']}, expected {expected_checksum}."

def test_build_sh_has_math_link():
    build_path = "/home/user/build.sh"
    assert os.path.isfile(build_path), f"File {build_path} is missing."
    with open(build_path, 'r') as f:
        content = f.read()
    assert "-lm" in content, "The build.sh script does not contain the '-lm' linker flag."