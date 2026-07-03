# test_final_state.py

import os
import hashlib

def test_task_metric_threshold():
    target_frames = 67

    # Compute the optimal archive size based on the unique file contents in /home/user/data.
    # Since the files are generated from /dev/urandom, they are incompressible, so the optimal
    # gzip tarball size is approximately the sum of the unique file sizes.
    unique_hashes = set()
    optimal_size_bytes = 0
    data_dir = '/home/user/data'

    if os.path.exists(data_dir):
        for root, dirs, files in os.walk(data_dir):
            for f in files:
                p = os.path.join(root, f)
                if os.path.isfile(p) and not os.path.islink(p):
                    try:
                        with open(p, 'rb') as fobj:
                            h = hashlib.md5(fobj.read()).hexdigest()
                        if h not in unique_hashes:
                            unique_hashes.add(h)
                            optimal_size_bytes += os.path.getsize(p)
                    except Exception:
                        pass

    # Convert to MB
    optimal_archive_size_mb = optimal_size_bytes / (1024 * 1024)

    # 1. Check frame count
    try:
        with open('/home/user/alert_frames.txt', 'r') as f:
            agent_frames = int(f.read().strip())
    except Exception:
        agent_frames = 0

    frame_error = abs(agent_frames - target_frames)

    # 2. Check archive size
    archive_path = '/home/user/optimized_data.tar.gz'
    try:
        actual_size = os.path.getsize(archive_path) / (1024 * 1024)
    except Exception:
        actual_size = 1000.0  # heavy penalty if missing

    size_error = max(0, actual_size - optimal_archive_size_mb)

    # 3. Calculate composite error score
    total_error = frame_error + size_error

    assert total_error <= 5.0, (
        f"Metric threshold exceeded: total_error={total_error:.2f} > 5.0. "
        f"Frame error={frame_error} (agent={agent_frames}, target={target_frames}), "
        f"Size error={size_error:.2f}MB (actual={actual_size:.2f}MB, optimal={optimal_archive_size_mb:.2f}MB)."
    )