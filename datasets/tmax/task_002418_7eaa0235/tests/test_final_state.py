# test_final_state.py
import os
import stat
import subprocess
import time
import pytest

def test_pipeline_script_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Pipeline script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {path} is not executable."

def test_dockerfile_exists():
    path = "/app/obs-dash-gen/Dockerfile"
    assert os.path.isfile(path), f"Dockerfile {path} does not exist."

def test_dashboard_generated():
    path = "/home/user/dashboard.html"
    assert os.path.isfile(path), f"Dashboard file {path} was not generated."
    assert os.path.getsize(path) > 0, f"Dashboard file {path} is empty."
    with open(path, 'r') as f:
        content = f.read()
    assert "html" in content.lower(), f"Dashboard file {path} does not appear to contain HTML."

def test_deploy_status():
    path = "/home/user/deploy_status.txt"
    assert os.path.isfile(path), f"Deploy status file {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert "200" in content, f"Deploy status file {path} does not contain '200'. Content: {content}"

def test_docker_image_exists():
    result = subprocess.run(
        ["docker", "images", "-q", "obs-dash:latest"],
        capture_output=True, text=True
    )
    assert result.stdout.strip(), "Docker image 'obs-dash:latest' was not built."

def test_parser_performance():
    # Metric test: measure wall-clock time of running the parser
    # The truth specifies: docker run --rm -v /home/user/system.log:/system.log obs-dash:latest /system.log
    # But since the entrypoint is main.py, we can just run the container and pass the file.

    log_file = "/home/user/system.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    start_time = time.time()
    result = subprocess.run(
        [
            "docker", "run", "--rm", 
            "-v", f"{log_file}:/system.log:ro", 
            "obs-dash:latest", "/system.log"
        ],
        capture_output=True, text=True
    )
    end_time = time.time()

    assert result.returncode == 0, f"Docker container execution failed with error: {result.stderr}"

    execution_time = end_time - start_time
    threshold = 2.0
    assert execution_time <= threshold, (
        f"Execution time {execution_time:.2f}s exceeded the threshold of {threshold}s. "
        "The parser regex optimization is likely insufficient or incorrect."
    )