# test_final_state.py
import subprocess
import os
import time
import socket
import pytest

def test_sanitizer_binary_corpus():
    # Ensure the C file exists
    c_file = '/home/user/sanitizer.c'
    assert os.path.exists(c_file), f"Sanitizer source code missing at {c_file}"

    # Compile the binary to be sure we are testing the latest code
    binary = '/home/user/sanitizer_test'
    compile_proc = subprocess.run(['gcc', c_file, '-o', binary], capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Compilation failed: {compile_proc.stderr}"

    clean_dir = '/app/tests/corpus/clean'
    evil_dir = '/app/tests/corpus/evil'

    # Test clean corpus
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)]
    for f in clean_files:
        with open(f, 'r') as fin:
            expected = fin.read().strip()

        with open(f, 'r') as fin:
            out = subprocess.check_output([binary], stdin=fin, text=True).strip()

        assert out == expected, f"Clean file {os.path.basename(f)} was modified or rejected. Expected:\n{expected}\nGot:\n{out}"

    # Test evil corpus
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)]
    for f in evil_files:
        with open(f, 'r') as fin:
            out = subprocess.check_output([binary], stdin=fin, text=True).strip()

        # The evil corpus contains exactly 1 valid row among the malicious ones
        assert "1,45.5,12.2,catA" in out, f"Valid row in {os.path.basename(f)} was incorrectly rejected."
        assert "NaN" not in out, f"Evil row with NaN in {os.path.basename(f)} bypassed sanitizer."
        assert "1000.1" not in out, f"Evil row with out-of-bounds value in {os.path.basename(f)} bypassed sanitizer."
        assert "toolongcategoryname" not in out, f"Evil row with long category in {os.path.basename(f)} bypassed sanitizer."
        assert "extra_column" not in out, f"Evil row with extra column in {os.path.basename(f)} bypassed sanitizer."
        assert "drop table" not in out, f"Evil row with non-numeric feature in {os.path.basename(f)} bypassed sanitizer."

def test_pipeline_integration():
    script_path = '/app/start_pipeline.sh'
    assert os.path.exists(script_path), f"Pipeline script missing at {script_path}"

    # Clean up any existing redis/nc processes
    subprocess.run(['pkill', '-f', 'redis-server'], check=False)
    subprocess.run(['pkill', '-f', 'nc'], check=False)
    subprocess.run(['redis-cli', 'del', 'clean_data'], check=False)

    # Start pipeline
    p = subprocess.Popen(['bash', script_path])
    time.sleep(3) # Wait for services to initialize

    try:
        # Send clean data
        clean_dir = '/app/tests/corpus/clean'
        for f in os.listdir(clean_dir):
            path = os.path.join(clean_dir, f)
            with open(path, 'rb') as fin:
                data = fin.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect(('127.0.0.1', 9000))
                s.sendall(data)
                s.close()
                time.sleep(0.5)

        # Send evil data
        evil_dir = '/app/tests/corpus/evil'
        for f in os.listdir(evil_dir):
            path = os.path.join(evil_dir, f)
            with open(path, 'rb') as fin:
                data = fin.read()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect(('127.0.0.1', 9000))
                s.sendall(data)
                s.close()
                time.sleep(0.5)
    except Exception as e:
        pytest.fail(f"Failed to send data to pipeline on port 9000: {e}")

    time.sleep(2) # Wait for processing and redis insertion

    try:
        out = subprocess.check_output(['redis-cli', 'lrange', 'clean_data', '0', '-1'], text=True)
        lines = [line.strip() for line in out.split('\n') if line.strip()]

        # We expect 3 rows from clean, and 1 valid row from evil
        assert len(lines) == 4, f"Expected exactly 4 valid rows in Redis 'clean_data' list, got {len(lines)}.\nContents: {lines}"
        assert "1,45.5,12.2,catA" in lines, "Missing expected row from clean/evil corpus"
        assert "2,-900.1,0.0,catB" in lines, "Missing expected row from clean corpus"
        assert "3,1000.0,-1000.0,catC" in lines, "Missing expected row from clean corpus"
    finally:
        p.kill()
        subprocess.run(['pkill', '-f', 'redis-server'], check=False)
        subprocess.run(['pkill', '-f', 'nc'], check=False)