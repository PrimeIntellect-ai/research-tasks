# test_final_state.py

import os
import time
import subprocess
import pytest

def test_executable_exists_and_is_executable():
    target_exe = "/home/user/dsp_processor_fixed"
    assert os.path.exists(target_exe), f"Executable {target_exe} does not exist."
    assert os.path.isfile(target_exe), f"Path {target_exe} is not a file."
    assert os.access(target_exe, os.X_OK), f"File {target_exe} is not executable."

def test_execution_time_and_output():
    target_exe = "/home/user/dsp_processor_fixed"
    input_wav = "/app/suspicious_audio.wav"
    output_wav = "/tmp/eval_out.wav"

    # Ensure input exists
    assert os.path.exists(input_wav), f"Input audio {input_wav} is missing."

    # Remove output if it exists from previous runs
    if os.path.exists(output_wav):
        os.remove(output_wav)

    start_time = time.time()
    try:
        result = subprocess.run(
            [target_exe, input_wav, output_wav],
            check=True,
            timeout=10,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution timed out. The denormal issue is likely not fixed.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executable crashed with return code {e.returncode}. Stderr: {e.stderr}")

    end_time = time.time()
    runtime = end_time - start_time

    assert os.path.exists(output_wav), f"Output file {output_wav} was not created."
    assert os.path.getsize(output_wav) > 0, f"Output file {output_wav} is empty."

    threshold = 0.2
    assert runtime <= threshold, f"Execution time {runtime:.4f}s exceeded the threshold of {threshold}s. The denormal issue is likely not fixed."