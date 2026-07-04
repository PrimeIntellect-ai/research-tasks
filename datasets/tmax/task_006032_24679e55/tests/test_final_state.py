# test_final_state.py

import os
import subprocess
import json
import pytest

def test_output_files_exist():
    """Test that the required output files have been created."""
    assert os.path.isfile('/home/user/anomalies.parquet'), "The file /home/user/anomalies.parquet was not created."
    assert os.path.isfile('/home/user/model_data.h5'), "The file /home/user/model_data.h5 was not created."

def test_parquet_contents():
    """Test the contents of the Parquet file using a subprocess to leverage pandas/pyarrow."""
    script = """
import sys
import json
try:
    import pandas as pd
    df = pd.read_parquet('/home/user/anomalies.parquet')
    res = {
        'len': len(df),
        'cols': list(df.columns)
    }
    print(json.dumps(res))
except Exception as e:
    print(json.dumps({'error': str(e)}))
"""
    try:
        out = subprocess.check_output([sys.executable, '-c', script], stderr=subprocess.STDOUT).decode('utf-8')
        data = json.loads(out.strip().split('\n')[-1])
    except Exception as e:
        pytest.fail(f"Failed to execute verification script for Parquet file: {e}")

    assert 'error' not in data, f"Error reading parquet file: {data.get('error')}"

    # IsolationForest with contamination=0.05 on 10,000 records should yield exactly 500 anomalies
    assert data['len'] == 500, f"Expected exactly 500 anomalous records, but found {data['len']}."

    expected_columns = {'transaction_id', 'amount', 'duration', 'location_score', 'network_latency', 'device_trust', 'pc1', 'pc2', 'pc3'}
    actual_columns = set(data['cols'])
    missing_columns = expected_columns - actual_columns
    assert not missing_columns, f"Missing columns in Parquet file: {missing_columns}. Found: {actual_columns}"

def test_hdf5_contents():
    """Test the contents of the HDF5 file using a subprocess to leverage h5py."""
    import sys
    script = """
import sys
import json
try:
    import h5py
    with h5py.File('/home/user/model_data.h5', 'r') as f:
        pca_components = f['pca_components'][:]
        res = {'shape': list(pca_components.shape)}
    print(json.dumps(res))
except Exception as e:
    print(json.dumps({'error': str(e)}))
"""
    try:
        out = subprocess.check_output([sys.executable, '-c', script], stderr=subprocess.STDOUT).decode('utf-8')
        data = json.loads(out.strip().split('\n')[-1])
    except Exception as e:
        pytest.fail(f"Failed to execute verification script for HDF5 file: {e}")

    assert 'error' not in data, f"Error reading HDF5 file: {data.get('error')}"

    expected_shape = [3, 5]
    actual_shape = data['shape']
    assert actual_shape == expected_shape, f"Expected PCA components shape {expected_shape}, but got {actual_shape}."