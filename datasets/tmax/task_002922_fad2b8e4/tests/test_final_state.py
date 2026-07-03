# test_final_state.py
import os
import subprocess
import re

def test_pipeline_files_exist():
    assert os.path.exists("/home/user/process_logs.c"), "/home/user/process_logs.c is missing."
    assert os.path.exists("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh is missing."
    assert os.access("/home/user/run_pipeline.sh", os.X_OK), "/home/user/run_pipeline.sh is not executable."

def test_pipeline_execution_and_output():
    # Execute the pipeline script to ensure it runs correctly and generates the output
    result = subprocess.run(
        ["/home/user/run_pipeline.sh"], 
        cwd="/home/user", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"run_pipeline.sh failed to execute. Stderr: {result.stderr}"

    csv_file = "/home/user/processed_logs.csv"
    assert os.path.exists(csv_file), f"{csv_file} was not created by the pipeline."

    # Compute expected output from the raw logs to verify correctness
    raw_file = "/home/user/raw_config_logs.txt"
    assert os.path.exists(raw_file), f"{raw_file} is missing."

    buckets = {}
    with open(raw_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse the log line: [EPOCH] KEY=VALUE IP
            m = re.match(r'^\[(\d+)\]\s+([^=]+)=([^\s]+)\s+(.*)$', line)
            assert m, f"Failed to parse raw log line: {line}"

            epoch = int(m.group(1))
            key = m.group(2)
            value = m.group(3)
            ip = m.group(4)

            window = (epoch // 3600) * 3600

            # Mask the IP address
            ip_parts = ip.split('.')
            ip_parts[-1] = 'XXX'
            masked_ip = '.'.join(ip_parts)

            dict_key = (window, key)
            # Deduplicate by keeping the largest epoch
            if dict_key not in buckets or buckets[dict_key][0] < epoch:
                buckets[dict_key] = (epoch, value, masked_ip)

    expected_lines = []
    for (window, key), (epoch, value, masked_ip) in buckets.items():
        expected_lines.append(f"{window},{key},{value},{masked_ip}")

    # Sort output: numerically by window, then alphabetically by key
    expected_lines.sort(key=lambda x: (int(x.split(',')[0]), x.split(',')[1]))
    expected_csv = "\n".join(expected_lines)

    with open(csv_file, "r") as f:
        actual_csv = f.read().strip()

    assert actual_csv == expected_csv, (
        f"Contents of {csv_file} do not match the expected output.\n"
        f"Expected:\n{expected_csv}\n\n"
        f"Actual:\n{actual_csv}"
    )