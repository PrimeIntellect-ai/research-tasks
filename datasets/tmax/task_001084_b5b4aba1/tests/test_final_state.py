# test_final_state.py

import os
import subprocess
import random
import tempfile
import re
import pytest

def get_truth_blacklist():
    """Extract subtitles from the video to get the truth blacklist."""
    try:
        # Run ffmpeg to extract the subtitle stream
        result = subprocess.run(
            ["ffmpeg", "-i", "/app/build_metrics.mp4", "-map", "0:1", "-f", "srt", "-"],
            capture_output=True,
            text=True,
            check=True
        )
        srt_content = result.stdout
        # Parse SRT to get just the text lines
        # SRT format:
        # 1
        # 00:00:00,000 --> 00:00:01,000
        # 1.2.3
        #
        lines = srt_content.strip().split('\n')
        blacklist = []
        for line in lines:
            line = line.strip()
            # Ignore numbers (index), timestamps, and empty lines
            if not line or '-->' in line or line.isdigit():
                continue
            # Remove any html-like tags if present
            clean_line = re.sub(r'<[^>]+>', '', line)
            blacklist.append(clean_line)
        return "\n".join(blacklist) + "\n" if blacklist else ""
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract subtitles from video using ffmpeg: {e.stderr}")

def test_blacklist_extracted_correctly():
    """Test that the blacklist was correctly extracted from the video."""
    blacklist_path = "/home/user/blacklist.txt"
    assert os.path.isfile(blacklist_path), f"Blacklist file missing at {blacklist_path}"

    with open(blacklist_path, "r") as f:
        user_blacklist = f.read()

    truth_blacklist = get_truth_blacklist()

    # Compare line by line, ignoring trailing whitespace
    user_lines = [line.strip() for line in user_blacklist.strip().split('\n') if line.strip()]
    truth_lines = [line.strip() for line in truth_blacklist.strip().split('\n') if line.strip()]

    assert user_lines == truth_lines, "The extracted blacklist does not match the subtitles in the video."

def generate_random_semver():
    """Generate a random semantic version string."""
    if random.random() < 0.1:
        # Malformed
        return f"{random.randint(0, 5)}.{random.randint(0, 5)}"
    return f"{random.randint(0, 5)}.{random.randint(0, 10)}.{random.randint(0, 20)}"

def generate_random_range():
    """Generate a random semver range."""
    ver = generate_random_semver()
    prefix = random.choice(["^", "~", ""])
    return f"{prefix}{ver}"

def test_resolve_artifacts_fuzz():
    """Fuzz test the resolve_artifacts.sh script against the oracle."""
    agent_script = "/home/user/resolve_artifacts.sh"
    oracle_script = "/app/oracle_resolve.sh"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable: {agent_script}"

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        # Generate available versions
        num_versions = random.randint(20, 100)
        available_versions = [generate_random_semver() for _ in range(num_versions)]

        # Write to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("\n".join(available_versions) + "\n")
            tmp_path = tmp.name

        try:
            req_range = generate_random_range()

            # Run Oracle
            oracle_res = subprocess.run(
                ["bash", oracle_script, req_range, tmp_path],
                capture_output=True,
                text=True
            )
            oracle_out = oracle_res.stdout.strip()

            # Run Agent
            agent_res = subprocess.run(
                ["bash", agent_script, req_range, tmp_path],
                capture_output=True,
                text=True
            )
            agent_out = agent_res.stdout.strip()

            assert agent_out == oracle_out, (
                f"Mismatch on test case {i+1}/{num_tests}.\n"
                f"Range: {req_range}\n"
                f"Available versions: {available_versions}\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}\n"
                f"Agent stderr: {agent_res.stderr}"
            )
        finally:
            os.remove(tmp_path)