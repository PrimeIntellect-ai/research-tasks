# test_final_state.py
import os
import subprocess
import tempfile
import pandas as pd
import numpy as np
import pytest

def test_fast_etl_correctness():
    cpp_file = "/home/user/fast_etl.cpp"
    assert os.path.exists(cpp_file), f"Source file {cpp_file} not found."

    executable = "/home/user/fast_etl"
    compile_cmd = ["g++", "-O3", "-std=c++17", cpp_file, "-o", executable]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation failed:\n{res.stderr}"

    with tempfile.TemporaryDirectory() as tmpdir:
        train_csv = os.path.join(tmpdir, "train.csv")
        test_csv = os.path.join(tmpdir, "test.csv")

        np.random.seed(42)
        train_df = pd.DataFrame({
            'id': range(1, 101),
            'category': np.random.choice(['A', 'B', 'C', 'D'], 100),
            'target': np.random.randn(100) * 10 + 50
        })
        test_df = pd.DataFrame({
            'id': range(101, 151),
            'category': np.random.choice(['A', 'B', 'C', 'E'], 50), # E is unseen
            'target': np.random.randn(50) * 10 + 50
        })
        train_df.to_csv(train_csv, index=False)
        test_df.to_csv(test_csv, index=False)

        run_cmd = [executable, "train.csv", "test.csv"]
        res = subprocess.run(run_cmd, cwd=tmpdir, capture_output=True, text=True)
        assert res.returncode == 0, f"Execution failed:\n{res.stderr}\n{res.stdout}"

        test_out_csv = os.path.join(tmpdir, "test_encoded.csv")
        assert os.path.exists(test_out_csv), "test_encoded.csv was not created in the working directory."

        # Calculate Gold Standard
        global_mean = train_df['target'].mean()
        cat_stats = train_df.groupby('category')['target'].agg(['count', 'mean']).reset_index()
        m = 15.0
        cat_stats['gold_encoded'] = (cat_stats['count'] * cat_stats['mean'] + m * global_mean) / (cat_stats['count'] + m)
        gold_map = dict(zip(cat_stats['category'], cat_stats['gold_encoded']))

        def map_gold(cat):
            return gold_map.get(cat, global_mean)

        test_df['gold'] = test_df['category'].apply(map_gold)

        agent_out = pd.read_csv(test_out_csv)
        assert 'id' in agent_out.columns and 'encoded_target' in agent_out.columns, "Output CSV missing required columns 'id' and 'encoded_target'."

        merged = pd.merge(test_df, agent_out, on='id')
        assert len(merged) == len(test_df), "Output row count mismatch or missing IDs."

        max_err = np.max(np.abs(merged['gold'] - merged['encoded_target']))
        threshold = 1e-4

        assert max_err <= threshold, f"Max AE metric {max_err} exceeds threshold {threshold}"