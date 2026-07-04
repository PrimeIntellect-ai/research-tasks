# test_final_state.py
import os
import stat
import subprocess
import configparser
import ast

PROJECT_DIR = "/home/user/project"

def test_services_ini_updated():
    ini_path = os.path.join(PROJECT_DIR, "services.ini")
    assert os.path.isfile(ini_path), "services.ini is missing."

    config = configparser.ConfigParser()
    config.read(ini_path)

    assert config.has_section("analytics-worker"), "Missing [analytics-worker] section."
    assert config.has_option("analytics-worker", "After"), "Missing 'After' directive in [analytics-worker]."

    after_val = config.get("analytics-worker", "After")
    assert after_val == "data-fetcher", f"Expected 'After=data-fetcher', got 'After={after_val}'"

def test_analytics_worker_retry_logic():
    worker_path = os.path.join(PROJECT_DIR, "analytics-worker.py")
    assert os.path.isfile(worker_path), "analytics-worker.py is missing."

    with open(worker_path, "r") as f:
        content = f.read()

    # Check for retry logic keywords
    assert "except " in content or "except:" in content or "Exception" in content, "No exception handling found in analytics-worker.py."
    assert "time.sleep(1)" in content or "time.sleep(1.0)" in content, "Missing time.sleep(1) in analytics-worker.py."
    assert "sys.exit(1)" in content or "exit(1)" in content, "Missing exit code 1 on failure in analytics-worker.py."

    # Basic check for loop
    assert "for " in content or "while " in content, "No loop construct found for retries in analytics-worker.py."

def test_run_pipeline_script_exists_and_executable():
    script_path = os.path.join(PROJECT_DIR, "run_pipeline.sh")
    assert os.path.isfile(script_path), "run_pipeline.sh is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), "run_pipeline.sh is not executable."

def test_run_pipeline_execution_and_status():
    script_path = os.path.join(PROJECT_DIR, "run_pipeline.sh")
    assert os.path.isfile(script_path), "run_pipeline.sh is missing."

    # Run the script
    result = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)

    # Check if status.txt was created and has correct content
    status_path = os.path.join(PROJECT_DIR, "status.txt")
    assert os.path.isfile(status_path), "status.txt was not created by run_pipeline.sh."

    with open(status_path, "r") as f:
        status_content = f.read().strip()

    assert status_content == "PIPELINE_SUCCESS", f"Expected PIPELINE_SUCCESS in status.txt, got '{status_content}'"

    # Check if log file was created
    log_path = os.path.join(PROJECT_DIR, "logs", "pipeline.log")
    assert os.path.isfile(log_path), "pipeline.log was not created in logs directory."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "Starting data-fetcher..." in log_content, "Log file missing data-fetcher startup message."
    assert "Starting analytics-worker..." in log_content, "Log file missing analytics-worker startup message."
    assert "All services completed successfully." in log_content, "Log file missing successful completion message."