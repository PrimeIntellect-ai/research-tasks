# test_final_state.py
import os
import subprocess
import tempfile

def test_executable_exists():
    executable = "/home/user/workspace/log_filter"
    assert os.path.isfile(executable), f"Executable missing: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_adversarial_corpus():
    executable = "/home/user/workspace/log_filter"
    evil_dir = "/home/user/hidden_corpus/evil/"
    clean_dir = "/home/user/hidden_corpus/clean/"

    evil_bypassed = []
    evil_total = 0
    if os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if not os.path.isfile(filepath):
                continue
            evil_total += 1
            with tempfile.NamedTemporaryFile() as out_f:
                result = subprocess.run([executable, "--test", filepath, out_f.name], capture_output=True)
                assert result.returncode == 0, f"Filter crashed on evil file {filename}"
                out_f.seek(0)
                output = out_f.read()
                if len(output.strip()) > 0:
                    evil_bypassed.append(filename)

    clean_modified = []
    clean_total = 0
    if os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if not os.path.isfile(filepath):
                continue
            clean_total += 1
            with tempfile.NamedTemporaryFile() as out_f:
                result = subprocess.run([executable, "--test", filepath, out_f.name], capture_output=True)
                assert result.returncode == 0, f"Filter crashed on clean file {filename}"
                out_f.seek(0)
                output = out_f.read()
                with open(filepath, 'rb') as in_f:
                    expected = in_f.read()
                if output != expected:
                    clean_modified.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {evil_total} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {clean_total} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)