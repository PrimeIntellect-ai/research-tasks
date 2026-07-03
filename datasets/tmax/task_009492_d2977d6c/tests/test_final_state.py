# test_final_state.py

import os
import subprocess
import tarfile
import tempfile

def test_pipeline_script_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution_and_results():
    script_path = "/home/user/pipeline.sh"

    # Run the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    tarball_path = "/home/user/remote_sync/results.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} does not exist."

    # Verify contents of the tarball
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Look for the CSV file
        csv_path = None
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    break
            if csv_path:
                break

        assert csv_path is not None, "No CSV file found in the extracted tarball."

        with open(csv_path, "r") as f:
            content = f.read().strip().splitlines()

        expected_content = [
            "id,total_value",
            "1,145.00",
            "2,245.00",
            "3,345.00",
            "4,445.00",
            "5,545.00"
        ]

        assert content == expected_content, f"CSV content does not match expected.\nExpected: {expected_content}\nGot: {content}"

def test_cpp_source_code():
    cpp_path = "/home/user/aggregate.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Check for threading primitives
    has_thread = "<thread>" in content or "std::thread" in content
    has_future = "<future>" in content or "std::async" in content or "std::promise" in content or "std::packaged_task" in content

    assert has_thread or has_future, "C++ program does not appear to use <thread> or <future> for parallel execution."