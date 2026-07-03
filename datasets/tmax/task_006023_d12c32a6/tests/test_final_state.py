# test_final_state.py
import os
import stat
import json
import subprocess

def test_optimize_script_exists_and_executable():
    """Test that /home/user/optimize.sh exists and is executable."""
    script_path = "/home/user/optimize.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_optimize_script_produces_correct_output():
    """Test that running optimize.sh produces the correct top_metrics.csv."""
    script_path = "/home/user/optimize.sh"
    input_path = "/home/user/metrics.jsonl"
    output_path = "/home/user/top_metrics.csv"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

    # Compute expected output
    expected_data = {}
    with open(input_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            host = record["host"]
            process = record["process"]
            memory_mb = float(record["memory_mb"])

            if host not in expected_data:
                expected_data[host] = (memory_mb, process)
            else:
                if memory_mb > expected_data[host][0]:
                    expected_data[host] = (memory_mb, process)

    expected_lines = []
    for host in sorted(expected_data.keys()):
        mem, proc = expected_data[host]
        # Format memory strictly to avoid floating point representation issues, though the truth uses tostring in jq
        # Wait, the truth uses jq's tostring which outputs the float as it is in the JSON.
        # Let's read the exact string from the JSON if possible, or just compare values.
        expected_lines.append(f"{host},{proc},{mem}")

    # Read actual output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        actual_parts = actual.split(",")
        expected_parts = expected.split(",")

        assert len(actual_parts) == 3, f"Line {i+1} in output is not properly formatted CSV: {actual}"

        assert actual_parts[0] == expected_parts[0], f"Host mismatch on line {i+1}: expected {expected_parts[0]}, got {actual_parts[0]}"
        assert actual_parts[1] == expected_parts[1], f"Process mismatch on line {i+1}: expected {expected_parts[1]}, got {actual_parts[1]}"

        # Compare memory as float to avoid formatting differences (e.g., 10.0 vs 10)
        actual_mem = float(actual_parts[2])
        expected_mem = float(expected_parts[2])
        assert abs(actual_mem - expected_mem) < 1e-6, f"Memory mismatch on line {i+1}: expected {expected_mem}, got {actual_mem}"