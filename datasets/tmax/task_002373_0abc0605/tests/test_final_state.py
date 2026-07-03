# test_final_state.py
import os
import subprocess
import pytest

def test_executable_exists():
    exe_path = "/home/user/videod_repo/videod"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}. Did you compile the code?"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable."

def test_processed_frames_log_exists():
    log_path = "/home/user/processed_frames.log"
    assert os.path.isfile(log_path), f"Output log file not found at {log_path}. Did you pipe the output?"

def test_memory_leak_fixed():
    exe_path = "/home/user/videod_repo/videod"
    video_path = "/app/incident_stream.mp4"

    cmd = ['/usr/bin/time', '-f', '%M', exe_path, video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # /usr/bin/time writes the format string to stderr
    try:
        lines = result.stderr.strip().split('\n')
        memory_kb_str = lines[-1]
        memory_kb = int(memory_kb_str)
    except (ValueError, IndexError):
        pytest.fail(f"Could not parse memory output from /usr/bin/time. Stderr was: {result.stderr}")

    threshold = 15000
    assert memory_kb <= threshold, f"Memory exceeded threshold: {memory_kb} KB > {threshold} KB. The memory leak is not fully resolved."

def test_formula_corrected():
    process_c_path = "/home/user/videod_repo/process.c"
    assert os.path.isfile(process_c_path), f"Source file not found at {process_c_path}"

    with open(process_c_path, "r") as f:
        content = f.read()

    # The correct formula should use + 0.114
    assert "+ 0.114" in content, "The YUV Luma calculation formula typo was not corrected to use '+ 0.114'."
    assert "- 0.114" not in content, "The YUV Luma calculation formula still contains the buggy '- 0.114'."