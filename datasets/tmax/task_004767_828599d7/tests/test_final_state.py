# test_final_state.py
import os
import struct
import numpy as np
import pytest

def read_compacted(filepath):
    # Format: uint64, uint16, uint16, double (20 bytes total)
    fmt = '<QHHd'
    record_size = struct.calcsize(fmt)
    records = []
    with open(filepath, 'rb') as f:
        while chunk := f.read(record_size):
            if len(chunk) == record_size:
                records.append(struct.unpack(fmt, chunk))
    return records

def test_compacted_telemetry_file():
    agent_file = '/home/user/compacted_telemetry.bin'
    truth_file = '/tmp/ground_truth.bin'

    assert os.path.isfile(agent_file), f"Agent output file {agent_file} does not exist. Did you save it to the correct path?"
    assert os.path.isfile(truth_file), f"Ground truth file {truth_file} does not exist. Environment may be corrupted."

    agent_records = read_compacted(agent_file)
    truth_records = read_compacted(truth_file)

    assert len(agent_records) == len(truth_records), \
        f"Count mismatch. Expected {len(truth_records)} valid records, got {len(agent_records)}."

    # Sort both by TIMESTAMP (index 0) to handle concurrent append disorder
    agent_records.sort(key=lambda x: x[0])
    truth_records.sort(key=lambda x: x[0])

    agent_values = np.array([r[3] for r in agent_records])
    truth_values = np.array([r[3] for r in truth_records])

    mse = np.mean((agent_values - truth_values)**2)

    assert mse <= 0.001, f"MSE threshold exceeded. Expected MSE <= 0.001, got {mse}. Ensure you are parsing the VALUE field correctly as a double."