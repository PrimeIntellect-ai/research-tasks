# test_final_state.py
import os
import subprocess

def test_parsed_data_log():
    log_path = "/home/user/parsed_data.log"
    assert os.path.isfile(log_path), f"Expected output file {log_path} does not exist. Did you redirect the output?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected = (
        "Sensor 10: 25\n"
        "Status: OK\n"
        "Malformed packet: length 50 exceeds payload\n"
        "Sensor 12: 26"
    )

    assert content == expected, f"Content of {log_path} does not match expected output.\nExpected:\n{expected}\nGot:\n{content}"

def test_script_execution():
    script_path = "/home/user/parse_pcap.py"
    pcap_path = "/home/user/traffic.pcap"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(pcap_path), f"PCAP file {pcap_path} does not exist."

    result = subprocess.run(["python3", script_path, pcap_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Script crashed or returned non-zero exit code. Stderr:\n{result.stderr}"

    expected = (
        "Sensor 10: 25\n"
        "Status: OK\n"
        "Malformed packet: length 50 exceeds payload\n"
        "Sensor 12: 26"
    )

    assert result.stdout.strip() == expected, "Script output does not match expected output when run directly."