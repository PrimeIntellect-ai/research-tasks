# test_final_state.py

import os
import time
import subprocess
import math
import struct
import pytest
import pandas as pd
import numpy as np

def get_expected_scores(pcap_path):
    """
    Parses the PCAP file and computes the expected hazard scores.
    Assumes each packet has a 16-byte payload at the end of the packet data.
    """
    scores = []
    with open(pcap_path, 'rb') as f:
        magic = f.read(4)
        if magic == b'\xd4\xc3\xb2\xa1':
            endian = '<'
        elif magic == b'\xa1\xb2\xc3\xd4':
            endian = '>'
        else:
            endian = '<'

        f.seek(24) # Skip global header
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            _, _, incl_len, _ = struct.unpack(f'{endian}IIII', hdr)
            pkt_data = f.read(incl_len)

            # The payload is the last 16 bytes of the packet
            payload = pkt_data[-16:]
            if len(payload) >= 3:
                b0, b1, b2 = payload[0], payload[1], payload[2]
                # Formula: score = (byte[0] ^ 0x5A) * 2.5 + (byte[1] << 2) - sqrt(byte[2])
                score = (b0 ^ 0x5A) * 2.5 + (b1 << 2) - math.sqrt(b2)
                scores.append(score)
            else:
                scores.append(0.0)
    return scores

def test_output_csv_mse():
    csv_path = "/home/user/output.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist. Did you run the processor?"

    # Read the CSV, handling potential headers gracefully
    df = pd.read_csv(csv_path, header=None)
    assert df.shape[1] >= 2, "CSV must contain at least two columns: packet_id and score"

    user_scores = pd.to_numeric(df.iloc[:, 1], errors='coerce').dropna().values

    pcap_path = "/home/user/data/ingress.pcap"
    expected_scores = np.array(get_expected_scores(pcap_path))

    assert len(user_scores) == len(expected_scores), \
        f"Expected {len(expected_scores)} scores, but found {len(user_scores)} valid scores in the CSV."

    mse = np.mean((user_scores - expected_scores) ** 2)
    assert mse <= 1e-5, f"Mean Squared Error (MSE) is {mse:.6f}, expected 0.0. The formula logic is still incorrect."

def test_execution_time():
    binary_path = "/home/user/telemetry_processor/target/release/telemetry_processor"
    assert os.path.exists(binary_path), \
        f"Compiled release binary not found at {binary_path}. Did you compile with `cargo build --release`?"

    pcap_path = "/home/user/data/ingress.pcap"
    output_path = "/home/user/test_perf_output.csv"

    start_time = time.time()
    result = subprocess.run([binary_path, pcap_path, output_path], capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, \
        f"Binary execution failed with return code {result.returncode}\nStderr: {result.stderr.decode()}"

    exec_time = end_time - start_time
    assert exec_time <= 2.0, \
        f"Execution time was {exec_time:.2f} seconds, expected <= 2.0 seconds. The concurrency bottleneck is not fully resolved."