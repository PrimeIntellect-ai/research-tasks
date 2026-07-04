# test_final_state.py

import os
import json
import pytest
import numpy as np

def test_output_exists():
    output_path = "/home/user/output.jsonl"
    assert os.path.exists(output_path), f"Output file is missing at {output_path}"
    assert os.path.isfile(output_path), f"Output path at {output_path} is not a file"

def test_embedding_mse():
    output_path = "/home/user/output.jsonl"
    ref_path = "/app/test/reference.jsonl"

    assert os.path.exists(output_path), f"Output file is missing at {output_path}"
    assert os.path.exists(ref_path), f"Reference file is missing at {ref_path}"

    # Load reference data
    ref_data = {}
    with open(ref_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            ref_data[obj['user_id']] = np.array(obj['embedding'], dtype=np.float32)

    # Load output data
    out_data = {}
    with open(output_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                out_data[obj['user_id']] = np.array(obj['embedding'], dtype=np.float32)
            except Exception as e:
                pytest.fail(f"Failed to parse line in output.jsonl: {line}. Error: {e}")

    # Check user_ids match
    ref_users = set(ref_data.keys())
    out_users = set(out_data.keys())

    missing_users = ref_users - out_users
    extra_users = out_users - ref_users

    assert not missing_users, f"Output is missing user_ids: {missing_users}"
    assert not extra_users, f"Output contains extra user_ids: {extra_users}"

    # Calculate MSE
    mses = []
    for uid in ref_users:
        ref_emb = ref_data[uid]
        out_emb = out_data[uid]

        assert len(ref_emb) == 32, f"Reference embedding for {uid} does not have 32 dimensions"
        assert len(out_emb) == 32, f"Output embedding for {uid} does not have 32 dimensions"

        mse = np.mean((ref_emb - out_emb) ** 2)
        mses.append(mse)

    overall_mse = float(np.mean(mses))
    threshold = 1e-5

    assert overall_mse <= threshold, f"Overall MSE {overall_mse} exceeds threshold {threshold}"

def test_go_source_exists():
    source_path = "/home/user/etl.go"
    assert os.path.exists(source_path), f"Go source file is missing at {source_path}"
    assert os.path.isfile(source_path), f"Go source path at {source_path} is not a file"

def test_go_binary_exists():
    binary_path = "/home/user/etl"
    assert os.path.exists(binary_path), f"Go binary is missing at {binary_path}"
    assert os.path.isfile(binary_path), f"Go binary path at {binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"Go binary at {binary_path} is not executable"