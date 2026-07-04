# test_final_state.py

import os
import subprocess
import time
import pytest

def test_fast_decode_performance_and_output():
    script_path = "/home/user/fast_decode.sh"
    audio_path = "/app/audio/telemetry.wav"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    start_time = time.time()
    try:
        result = subprocess.run(
            ["/bin/bash", script_path, audio_path],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Script execution timed out after 10 seconds. Threshold is 2.0 seconds.")

    runtime = time.time() - start_time
    output = result.stdout.strip()

    expected = "libcore-2.1.0 libnet-1.4.2"
    assert output == expected, f"Script output did not match expected.\nExpected: '{expected}'\nGot: '{output}'"
    assert runtime <= 2.0, f"Script execution took {runtime:.3f} seconds, which exceeds the 2.0 seconds threshold."

def test_makefile_compilation():
    src_dir = "/app/src"
    makefile_path = os.path.join(src_dir, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    # Force a rebuild to ensure the Makefile changes actually work
    result = subprocess.run(
        ["make", "-B"],
        cwd=src_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Running 'make' failed. The Makefile might still have incorrect paths.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    main_exec = os.path.join(src_dir, "main")
    assert os.path.isfile(main_exec), f"Executable 'main' was not created after running make."
    assert os.access(main_exec, os.X_OK), f"File 'main' was created but is not executable."