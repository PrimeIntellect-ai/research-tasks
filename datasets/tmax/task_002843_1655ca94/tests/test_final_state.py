# test_final_state.py
import os
import glob
import time
import subprocess
import stat

def test_config_exists():
    config_path = "/etc/telemetry/settings.conf"
    assert os.path.exists(config_path), f"Config file {config_path} was not created to fix the segfault."

def test_plugin_compiled():
    plugin_so = "/home/user/plugin/parser_plugin.so"
    assert os.path.exists(plugin_so), f"Compiled plugin {plugin_so} does not exist. Did you compile it correctly?"

def test_wrapper_script_exists_and_executable():
    script_path = "/home/user/run_diagnostics.sh"
    assert os.path.exists(script_path), f"Wrapper script {script_path} not found."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script {script_path} is not executable."

def test_wrapper_script_performance_and_correctness():
    script_path = "/home/user/run_diagnostics.sh"
    target_dir = "/app/data"

    # Clear any previous runs to ensure we measure the actual script execution
    for f in glob.glob(f"{target_dir}/*.processed"):
        os.remove(f)

    start_time = time.time()
    result = subprocess.run([script_path, target_dir], capture_output=True, text=True)
    end_time = time.time()

    elapsed = end_time - start_time

    # Check if all files were processed
    processed_files = glob.glob(f"{target_dir}/*.processed")

    assert len(processed_files) == 1000, f"Error: Only {len(processed_files)}/1000 files were processed. Script output: {result.stderr}\n{result.stdout}"

    # Metric threshold assertion
    assert elapsed <= 5.0, f"Performance requirement failed. Execution time was {elapsed:.2f} seconds, which is > 5.0 seconds threshold. Ensure you are processing files concurrently."