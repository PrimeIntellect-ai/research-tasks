# test_final_state.py
import os
import subprocess

def test_resolution_txt():
    res_path = "/home/user/resolution.txt"
    assert os.path.isfile(res_path), f"File {res_path} does not exist."

    with open(res_path, "r") as f:
        content = f.read().strip()

    expected = "Crash Reason: OOMKilled_Memory_Limit_Exceeded\nAttacker IP: 10.45.99.12"
    assert content == expected, f"Content of {res_path} does not match the expected format and values. Found:\n{content}"

def test_process_logs_script_fixed():
    script_path = "/home/user/debug_env/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "$(ls logs/*.log)" not in content, "The script still contains the buggy '$(ls logs/*.log)' construct which breaks on spaces."

def test_script_execution_and_combined_output():
    script_path = "/home/user/debug_env/process_logs.sh"

    # Run the script
    result = subprocess.run(
        ["bash", script_path],
        cwd="/home/user/debug_env",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with exit code {result.returncode}.\nStderr: {result.stderr}"

    combined_path = "/home/user/debug_env/combined.txt"
    assert os.path.isfile(combined_path), f"File {combined_path} was not created after script execution."

    with open(combined_path, "r") as f:
        combined_content = f.read()

    assert "OOMKilled_Memory_Limit_Exceeded" in combined_content, "combined.txt does not contain the crash reason. The script might not be processing files with spaces correctly."
    assert "High latency detected." in combined_content, "combined.txt does not contain the performance monitor log."

def test_env_fixed():
    env_path = "/home/user/debug_env/.env"
    assert os.path.isfile(env_path), f"Environment file {env_path} does not exist."

    with open(env_path, "r") as f:
        content = f.read()

    assert "--invalid-flag-MALICIOUS" not in content, ".env file still contains the invalid flag."

    malicious_packets_path = "/home/user/debug_env/malicious_packets.txt"
    assert os.path.isfile(malicious_packets_path), f"File {malicious_packets_path} was not created."

    with open(malicious_packets_path, "r") as f:
        malicious_content = f.read()

    assert "MALICIOUS_PAYLOAD" in malicious_content, "malicious_packets.txt does not contain the expected malicious payload. The PCAP_FILTER_TERM in .env might still be incorrect."