# test_final_state.py

import os
import json
import struct
import random
import subprocess
import tempfile
import pytest

def test_parser_accuracy():
    parser_path = "/home/user/parser.py"
    assert os.path.exists(parser_path), f"Parser script not found at {parser_path}"

    num_files = 10000
    expected_ground_truth = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_files):
            filename = f"test_file_{i}.dat"
            filepath = os.path.join(tmpdir, filename)

            xor_key = random.randint(0, 0xFFFFFFFF)
            project_id = random.randint(0, 10000)
            timestamp = random.randint(1600000000, 1700000000)

            encoded_pid = project_id ^ xor_key
            encoded_ts = timestamp ^ xor_key

            file_type_idx = project_id % 3
            file_types = ["log", "media", "document"]
            file_type = file_types[file_type_idx]

            with open(filepath, "wb") as f:
                f.write(struct.pack(">IIII", 0xDEADBEEF, xor_key, encoded_pid, encoded_ts))
                # Add some random padding data to simulate real files
                f.write(os.urandom(random.randint(10, 50)))

            expected_ground_truth[filename] = {
                "project_id": project_id,
                "file_type": file_type,
                "timestamp": timestamp
            }

        # Run agent's script
        try:
            subprocess.run(["python3", parser_path, tmpdir], check=True, cwd=tmpdir, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"parser.py failed to execute: {e.stderr}")

        report_path = os.path.join(tmpdir, "metadata_report.json")
        assert os.path.exists(report_path), f"metadata_report.json not found in {tmpdir}"

        with open(report_path) as f:
            try:
                agent_output = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("metadata_report.json is not valid JSON")

        correct = 0
        for filename, expected_meta in expected_ground_truth.items():
            if filename in agent_output:
                agent_meta = agent_output[filename]
                if (agent_meta.get("project_id") == expected_meta["project_id"] and 
                    agent_meta.get("file_type") == expected_meta["file_type"] and 
                    agent_meta.get("timestamp") == expected_meta["timestamp"]):
                    correct += 1

        accuracy = correct / num_files
        assert accuracy >= 1.0, f"Accuracy {accuracy} below threshold 1.0. Correctly parsed {correct} out of {num_files} files."

def test_organized_data_exists():
    organized_dir = "/home/user/organized_data"
    assert os.path.exists(organized_dir), f"Organized data directory not found at {organized_dir}"
    assert os.path.isdir(organized_dir), f"{organized_dir} is not a directory"

    # Ensure that some files were moved/organized
    organized_files = []
    for root, dirs, files in os.walk(organized_dir):
        for f in files:
            if f.endswith(".dat"):
                organized_files.append(os.path.join(root, f))

    assert len(organized_files) > 0, "No .dat files found in the organized_data directory."