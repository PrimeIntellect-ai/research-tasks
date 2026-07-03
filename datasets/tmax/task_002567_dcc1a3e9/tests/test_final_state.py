# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_red_frames_count():
    """Verify that the red frames count is exactly 27."""
    output_file = "/home/user/red_frames.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run the video analysis?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "27", f"Expected exactly 27 red frames, but got '{content}' in {output_file}."

def test_manifest_sanitiser_corpus():
    """Verify the manifest sanitiser correctly classifies the adversarial corpus."""
    script_path = "/home/user/validate_manifests.py"
    assert os.path.isfile(script_path), f"Sanitiser script {script_path} is missing."

    clean_files = glob.glob("/app/corpus/clean/*.json")
    evil_files = glob.glob("/app/corpus/evil/*.json")

    assert len(clean_files) > 0, "Clean corpus is empty or missing."
    assert len(evil_files) > 0, "Evil corpus is empty or missing."

    clean_failed = []
    for clean_file in clean_files:
        result = subprocess.run(["/usr/bin/python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    evil_failed = []
    for evil_file in evil_files:
        result = subprocess.run(["/usr/bin/python3", script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(evil_file))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}{'...' if len(clean_failed) > 5 else ''}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed[:5])}{'...' if len(evil_failed) > 5 else ''}")

    assert not error_messages, "Adversarial corpus verification failed:\n" + "\n".join(error_messages)

def test_forward_script_and_cron():
    """Verify the port forwarding script exists and is scheduled in crontab."""
    script_path = "/home/user/forward.py"
    assert os.path.isfile(script_path), f"Port forward script {script_path} is missing."

    # Check if it's a valid python script (basic syntax check)
    syntax_check = subprocess.run(["/usr/bin/python3", "-m", "py_compile", script_path], capture_output=True)
    assert syntax_check.returncode == 0, f"Syntax error in {script_path}:\n{syntax_check.stderr.decode()}"

    # Check crontab
    crontab_check = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert crontab_check.returncode == 0, "Failed to read crontab. Has it been initialized for the user?"

    cron_lines = [line.strip() for line in crontab_check.stdout.splitlines() if line.strip() and not line.startswith("#")]

    # Look for the specific schedule and script
    found_cron = False
    for line in cron_lines:
        if "* * * * *" in line and script_path in line and "python3" in line:
            found_cron = True
            break

    assert found_cron, f"Could not find the expected cron job running {script_path} every minute (* * * * *). Found crontab: {crontab_check.stdout}"