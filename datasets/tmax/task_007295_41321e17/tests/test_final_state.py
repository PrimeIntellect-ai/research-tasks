# test_final_state.py
import os
import math

def test_process_c_exists():
    assert os.path.isfile("/home/user/process.c"), "The C program /home/user/process.c is missing."

def test_pipeline_sh_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_sampled_output():
    input_path = "/home/user/sensors.csv"
    output_path = "/home/user/sampled_output.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Compute expected output
    seen_hashes = set()
    stratum_counts = {0: 0, 1: 0, 2: 0}
    expected_records = []

    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            x, y, z = float(parts[0]), float(parts[1]), float(parts[2])

            # Calculate distance and cast to int
            dist = math.sqrt(x**2 + y**2 + z**2)
            int_dist = int(dist)

            # Calculate Stratum
            stratum = int_dist % 3

            # Calculate Hash
            h = int(x) ^ int(y) ^ int(z)

            # Deduplicate by Hash
            if h in seen_hashes:
                continue
            seen_hashes.add(h)

            # Sample exactly 2 per Stratum
            if stratum_counts[stratum] < 2:
                stratum_counts[stratum] += 1
                formatted_record = f"{stratum},{h},{x:.2f},{y:.2f},{z:.2f}"
                expected_records.append((stratum, formatted_record))

    # Sort by Stratum ascending (preserving original order within stratum)
    expected_records.sort(key=lambda item: item[0])
    expected_lines = [item[1] for item in expected_records]
    expected_content = "\n".join(expected_lines) + "\n"

    # Read actual output
    with open(output_path, "r") as f:
        actual_content = f.read()

    # Compare
    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Actual:\n{actual_content.strip()}"
    )