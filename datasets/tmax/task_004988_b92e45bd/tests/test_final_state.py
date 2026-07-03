# test_final_state.py
import h5py
import numpy as np
import os
import pytest

def test_density_h5_metric():
    """Test that the agent's HDF5 output matches the reference within the MSE threshold."""
    agent_file = '/home/user/density_out.h5'
    ref_file = '/app/reference_density.h5'

    assert os.path.exists(agent_file), f"Expected output file not found: {agent_file}"
    assert os.path.exists(ref_file), f"Reference file not found: {ref_file}"

    try:
        with h5py.File(agent_file, 'r') as f_agent, h5py.File(ref_file, 'r') as f_ref:
            assert 'electron_density' in f_agent, "Dataset 'electron_density' not found in agent's HDF5 file."
            assert 'electron_density' in f_ref, "Dataset 'electron_density' not found in reference HDF5 file."

            agent_data = f_agent['electron_density'][:]
            ref_data = f_ref['electron_density'][:]

            assert agent_data.shape == ref_data.shape, f"Shape mismatch: agent {agent_data.shape} vs ref {ref_data.shape}"

            mse = np.mean((agent_data - ref_data) ** 2)
            assert mse <= 1e-6, f"MSE {mse} exceeds threshold 1e-6"
    except Exception as e:
        pytest.fail(f"Failed to read and evaluate HDF5 files: {e}")

def test_fasta_exists():
    """Test that the extracted FASTA file exists and is not empty."""
    fasta_file = '/home/user/extracted_chain.fasta'
    assert os.path.exists(fasta_file), f"Expected FASTA file not found: {fasta_file}"
    assert os.path.getsize(fasta_file) > 0, f"FASTA file is empty: {fasta_file}"