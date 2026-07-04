# test_final_state.py
import os
import stat
import urllib.request
import numpy as np
from scipy.io import wavfile

def test_processor_c_exists():
    path = "/home/user/processor.c"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a regular file."

def test_deploy_sh_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a regular file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_server_running():
    pid_file = "/home/user/server.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

    # Check if web server is serving on port 8080
    try:
        response = urllib.request.urlopen("http://localhost:8080/")
        assert response.status == 200, f"Web server returned status {response.status} instead of 200."
    except Exception as e:
        assert False, f"Failed to connect to web server on port 8080: {e}"

def test_output_wav_mse():
    input_path = "/app/input.wav"
    output_path = "/home/user/output.wav"

    assert os.path.exists(output_path), f"File {output_path} does not exist."

    try:
        sr1, data_in = wavfile.read(input_path)
    except Exception as e:
        assert False, f"Failed to read input WAV file: {e}"

    try:
        sr2, data_out = wavfile.read(output_path)
    except Exception as e:
        assert False, f"Failed to read output WAV file: {e}"

    assert sr1 == sr2, f"Sample rates do not match: {sr1} != {sr2}"
    assert len(data_in) == len(data_out), f"Data lengths do not match: {len(data_in)} != {len(data_out)}"

    expected = (data_in * 0.5).astype(np.int16)
    mse = np.mean((expected.astype(float) - data_out.astype(float))**2)

    threshold = 1.0
    assert mse <= threshold, f"MSE {mse} is greater than threshold {threshold}"