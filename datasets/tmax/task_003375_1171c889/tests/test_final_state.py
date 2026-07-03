# test_final_state.py

import os
import time
import subprocess
import tempfile
import fcntl

def test_archiver_fixes():
    core_py = "/app/py-archiver-1.0.0/pyarchiver/core.py"

    # 1. Verify that the agent actually modified the source code to include fcntl locking
    assert os.path.isfile(core_py), f"Core module {core_py} is missing."
    with open(core_py, "r") as f:
        content = f.read()

    assert "fcntl" in content, "The 'fcntl' module is not imported or used in core.py."
    assert "flock" in content, "The 'fcntl.flock' method is not used in core.py for file locking."

    # 2. Verify performance and correctness (Recursive traversal + Buffer optimization)
    with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_dir:
        # Create 50MB of dummy data in subdirectories to test recursive traversal
        total_size_mb = 50.0
        num_subdirs = 5
        files_per_subdir = 2
        file_size_bytes = int((total_size_mb * 1024 * 1024) / (num_subdirs * files_per_subdir))

        for i in range(num_subdirs):
            sub = os.path.join(src_dir, f"sub_{i}")
            os.makedirs(sub)
            for j in range(files_per_subdir):
                file_path = os.path.join(sub, f"file_{j}.dat")
                with open(file_path, "wb") as f:
                    f.write(os.urandom(file_size_bytes))

        env = os.environ.copy()
        # Ensure the vendored package is in the Python path
        env["PYTHONPATH"] = "/app/py-archiver-1.0.0"

        start = time.time()
        res = subprocess.run(
            ["python", "-m", "pyarchiver.cli", "--source", src_dir, "--dest", dest_dir, "--chunk-size", "5MB"],
            env=env,
            capture_output=True,
            text=True
        )
        end = time.time()

        assert res.returncode == 0, f"Archiver execution failed with error:\n{res.stderr}"

        # Ensure that the archiver actually processed the files in subdirectories
        dest_files = os.listdir(dest_dir)
        assert len(dest_files) > 0, "No files were created in the destination directory. Recursive traversal may be failing."

        # Calculate throughput
        duration = end - start
        assert duration > 0, "Execution time was zero, cannot calculate throughput."
        throughput = total_size_mb / duration

        # Check against the threshold
        assert throughput >= 20.0, f"Throughput is too low: {throughput:.2f} MB/s. Expected at least 20.0 MB/s. Buffer size may not be optimized."