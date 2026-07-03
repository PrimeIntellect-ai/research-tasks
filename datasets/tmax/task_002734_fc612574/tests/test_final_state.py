# test_final_state.py
import os
import time
import subprocess
import numpy as np
import pytest

def generate_test_mesh(path, num_points):
    try:
        import h5py
        with h5py.File(path, 'w') as f:
            f.create_dataset('/coordinates', data=np.random.rand(num_points, 3).astype(np.float64))
    except ImportError:
        # Fallback if h5py is not available, though it should be given the task
        pass

def read_partition_ids(path):
    import h5py
    with h5py.File(path, 'r') as f:
        return f['/partition_ids'][:]

def test_fast_partitioner_speedup_and_correctness():
    fast_bin = "/home/user/fast_partitioner"
    legacy_bin = "/app/legacy_partitioner"
    mesh_path = "/home/user/mesh_data.h5"
    out_path = "/home/user/optimized_partitions.h5"
    legacy_out_path = "/tmp/legacy_out.h5"

    assert os.path.exists(fast_bin), f"Agent executable not found at {fast_bin}"
    assert os.access(fast_bin, os.X_OK), f"Agent executable {fast_bin} is not executable"

    # Generate a larger test mesh to properly measure speedup
    num_points = 200000
    try:
        import h5py
        generate_test_mesh(mesh_path, num_points)
    except ImportError:
        pass # use existing mesh if h5py is somehow missing

    # Run legacy partitioner
    if os.path.exists(out_path):
        os.remove(out_path)

    start_time = time.time()
    subprocess.run([legacy_bin], check=True)
    legacy_time = time.time() - start_time

    assert os.path.exists(out_path), "Legacy partitioner did not produce output"
    os.rename(out_path, legacy_out_path)

    # Run agent's fast partitioner
    start_time = time.time()
    subprocess.run([fast_bin], check=True)
    agent_time = time.time() - start_time

    assert os.path.exists(out_path), f"Agent partitioner did not produce output at {out_path}"

    # Verify correctness
    try:
        import h5py
        legacy_ids = read_partition_ids(legacy_out_path)
        agent_ids = read_partition_ids(out_path)
        np.testing.assert_array_equal(
            agent_ids, legacy_ids,
            err_msg="Agent's partition IDs do not match the legacy tool's output."
        )
    except ImportError:
        # Fallback to h5diff if h5py is not available
        result = subprocess.run(["h5diff", legacy_out_path, out_path, "/partition_ids", "/partition_ids"], capture_output=True)
        assert result.returncode == 0, f"Outputs differ according to h5diff:\n{result.stdout.decode()}"

    # Verify speedup
    speedup = legacy_time / agent_time
    assert speedup >= 3.0, f"Speedup is {speedup:.2f}x (Legacy: {legacy_time:.3f}s, Agent: {agent_time:.3f}s). Target is >= 3.0x."