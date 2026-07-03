# test_final_state.py

import os
import subprocess
import json
import pytest

def test_yq_installed():
    """Verify yq is installed and accessible."""
    yq_path = "/home/user/.local/bin/yq"
    assert os.path.isfile(yq_path), f"{yq_path} not found. Did you install yq locally?"
    assert os.access(yq_path, os.X_OK), f"{yq_path} is not executable."

    result = subprocess.run([yq_path, "--version"], capture_output=True, text=True)
    assert "yq 3.2.3" in result.stdout or "yq 3.2.3" in result.stderr, f"Expected yq 3.2.3, got {result.stdout.strip()} {result.stderr.strip()}"

def test_pipeline_script_exists():
    """Verify pipeline.sh exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cron_job_configured():
    """Verify the cron job is configured correctly."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Is it configured?"

    expected_cron = "*/15 * * * * /home/user/pipeline.sh /app/incoming_logs /home/user/processed_logs"
    assert expected_cron in result.stdout, f"Crontab does not contain the expected entry. Found:\n{result.stdout}"

def get_json_lines(file_path):
    if not os.path.isfile(file_path):
        return []
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    res = []
    for line in lines:
        if line.strip():
            try:
                res.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return res

def test_adversarial_corpus_evil():
    """Verify that all evil logs are rejected."""
    script_path = "/home/user/pipeline.sh"
    evil_in = "/app/corpora/evil"
    evil_out = "/tmp/evil_out"

    os.makedirs(evil_out, exist_ok=True)
    result = subprocess.run([script_path, evil_in, evil_out], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed on evil corpus:\n{result.stderr}"

    out_file = os.path.join(evil_out, "cleaned.json")
    lines = get_json_lines(out_file)
    assert len(lines) == 0, f"Evil logs bypassed the filter. Found {len(lines)} logs in output."

def test_adversarial_corpus_clean():
    """Verify that all clean logs are preserved and deduplicated."""
    script_path = "/home/user/pipeline.sh"
    clean_in = "/app/corpora/clean"
    clean_out = "/tmp/clean_out"

    os.makedirs(clean_out, exist_ok=True)
    result = subprocess.run([script_path, clean_in, clean_out], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed on clean corpus:\n{result.stderr}"

    out_file = os.path.join(clean_out, "cleaned.json")
    assert os.path.isfile(out_file), f"Output file {out_file} not created."

    output_lines = get_json_lines(out_file)

    # Compute expected clean output
    expected = []
    seen_ids = set()
    for root, _, files in os.walk(clean_in):
        for file in sorted(files):
            if file.endswith('.json'):
                lines = get_json_lines(os.path.join(root, file))
                for obj in lines:
                    req_id = obj.get("request_id")
                    if req_id not in seen_ids:
                        seen_ids.add(req_id)
                        expected.append(obj)

    assert len(output_lines) == len(expected), f"Clean logs modified or dropped. Expected {len(expected)}, got {len(output_lines)}."
    for out_obj, exp_obj in zip(output_lines, expected):
        assert out_obj == exp_obj, f"Output log {out_obj} does not match expected {exp_obj}."