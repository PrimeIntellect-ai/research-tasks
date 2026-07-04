# test_final_state.py
import os
import glob
import subprocess
import json
import pytest

def get_filter_cmd():
    env_file = "/home/user/solution.env"
    if not os.path.exists(env_file):
        return None
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("FILTER_CMD="):
                val = line.strip().split("=", 1)[1]
                return val.strip('"\'')
    return None

def test_solution_env_and_filter_executable():
    cmd = get_filter_cmd()
    assert cmd is not None, "FILTER_CMD not found in /home/user/solution.env"
    assert os.path.isabs(cmd), f"FILTER_CMD path '{cmd}' is not absolute"
    assert os.path.exists(cmd), f"Filter script not found at {cmd}"
    assert os.access(cmd, os.X_OK), f"Filter script at {cmd} is not executable"

def test_adversarial_corpus_filtering():
    cmd = get_filter_cmd()
    assert cmd is not None, "Cannot test corpus without FILTER_CMD"

    evil_dir = "/home/user/app/corpora/evil/"
    clean_dir = "/home/user/app/corpora/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    for e_file in evil_files:
        with open(e_file, "r") as f:
            content = f.read()
        proc = subprocess.run([cmd], input=content, text=True, capture_output=True)
        if proc.stdout.strip():
            evil_bypassed.append(os.path.basename(e_file))

    for c_file in clean_files:
        with open(c_file, "r") as f:
            content = f.read()
        proc = subprocess.run([cmd], input=content, text=True, capture_output=True)

        input_lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        output_lines = [line.strip() for line in proc.stdout.strip().split('\n') if line.strip()]

        if len(input_lines) != len(output_lines):
            clean_modified.append(os.path.basename(c_file))
            continue

        is_modified = False
        for il, ol in zip(input_lines, output_lines):
            try:
                if json.loads(il) != json.loads(ol):
                    is_modified = True
                    break
            except json.JSONDecodeError:
                is_modified = True
                break

        if is_modified:
            clean_modified.append(os.path.basename(c_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msg, " ; ".join(error_msg)

def test_systemd_configuration():
    cmd = ["systemctl", "--user", "show", "cost-aggregator.service", "-p", "After", "-p", "Requires", "-p", "Restart"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stdout

    assert "billing-receiver.service" in output, "cost-aggregator.service is missing dependency on billing-receiver.service (After/Requires)"
    assert "Restart=always" in output, "cost-aggregator.service is missing Restart=always"

def test_pipeline_integration():
    script_path = "/home/user/app/run-aggregator.sh"
    assert os.path.exists(script_path), f"Aggregator script not found at {script_path}"
    with open(script_path, "r") as f:
        content = f.read()

    cmd = get_filter_cmd()
    assert cmd is not None, "Cannot verify pipeline without FILTER_CMD"

    basename = os.path.basename(cmd)
    assert cmd in content or basename in content, f"run-aggregator.sh does not appear to pipe through the cost-filter ({basename})"