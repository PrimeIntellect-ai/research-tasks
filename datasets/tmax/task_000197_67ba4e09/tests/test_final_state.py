# test_final_state.py
import os
import subprocess
import hashlib
import time

def test_red_frame_count():
    path = "/home/user/red_frame_count.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "14", f"Expected red frame count to be '14', but got '{content}'"

def test_sanitizer_script():
    script_path = "/home/user/sanitizer.sh"
    assert os.path.isfile(script_path), f"Missing required script: {script_path}"

    evil_corpus = "/app/corpus/evil"
    clean_corpus = "/app/corpus/clean"

    evil_bypassed = []
    if os.path.isdir(evil_corpus):
        for item in os.listdir(evil_corpus):
            item_path = os.path.join(evil_corpus, item)
            if os.path.isdir(item_path):
                result = subprocess.run(["/bin/bash", script_path, item_path], capture_output=True)
                if result.returncode != 1:
                    evil_bypassed.append(item)

    clean_modified = []
    if os.path.isdir(clean_corpus):
        for item in os.listdir(clean_corpus):
            item_path = os.path.join(clean_corpus, item)
            if os.path.isdir(item_path):
                result = subprocess.run(["/bin/bash", script_path, item_path], capture_output=True)
                if result.returncode != 0:
                    clean_modified.append(item)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_msgs, "Sanitizer script failed on corpora: " + "; ".join(error_msgs)

def test_failed_dat_manifest():
    manifest_path = "/home/user/failed_dat_manifest.txt"
    assert os.path.isfile(manifest_path), f"Missing required file: {manifest_path}"

    log_path = "/app/backup_runs.log"
    targets = []
    if os.path.isfile(log_path):
        with open(log_path, 'r') as f:
            content = f.read().split('--')
            for block in content:
                lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
                target = None
                status = None
                for line in lines:
                    if line.startswith('Target:'):
                        target = line.split(':', 1)[1].strip()
                    elif line.startswith('Status:'):
                        status = line.split(':', 1)[1].strip()
                if status == 'FAILED' and target:
                    targets.append(target)

    expected_lines = []
    for target in targets:
        if os.path.isdir(target):
            try:
                # Use find to match bash behavior exactly
                output = subprocess.check_output(["find", target, "-type", "f", "-name", "*.dat", "-mtime", "-7"], text=True).strip()
                if output:
                    for filepath in output.split('\n'):
                        if os.path.isfile(filepath):
                            with open(filepath, 'rb') as f:
                                h = hashlib.sha256(f.read()).hexdigest()
                            expected_lines.append(f"{h}  {filepath}")
            except subprocess.CalledProcessError:
                pass

    expected_lines.sort(key=lambda x: x.split("  ")[1])
    expected_manifest = "\n".join(expected_lines) + "\n" if expected_lines else ""

    with open(manifest_path, "r") as f:
        actual_manifest = f.read()

    assert actual_manifest.strip() == expected_manifest.strip(), "Manifest content does not match expected output."