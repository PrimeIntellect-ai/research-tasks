# test_final_state.py

import os
import subprocess
import re
import pytest

def test_sensor_processor_cpp_exists():
    """Verify that the C++ source file exists."""
    cpp_path = "/home/user/edge_app/sensor_processor.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

def test_run_pipeline_script():
    """Run the pipeline script and verify the processed output."""
    script_path = "/home/user/edge_app/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Execute the pipeline script
    result = subprocess.run(
        ["/bin/bash", script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run_pipeline.sh failed with error: {result.stderr}"

    # Verify the output file
    output_path = "/home/user/data/processed_sensors.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_output = (
        "[temp_02] recorded 46.0\n"
        "[press_01] recorded 100.5\n"
        "[temp_03] recorded 45.6"
    )

    assert content == expected_output, (
        f"Content of {output_path} does not match expected output.\n"
        f"Expected:\n{expected_output}\nGot:\n{content}"
    )

def test_system_fstab():
    """Verify the custom fstab entry is correct."""
    fstab_path = "/home/user/system_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} is missing."

    with open(fstab_path, "r") as f:
        lines = f.readlines()

    found_entry = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            if (parts[0] == "/home/user/sensor_disk.img" and
                parts[1] == "/home/user/data" and
                parts[2] == "ext4" and
                parts[3] == "rw,user,noatime" and
                parts[4] == "0" and
                parts[5] == "2"):
                found_entry = True
                break

    assert found_entry, "Correct fstab entry for sensor_disk.img was not found in /home/user/system_fstab."

def test_nginx_lb_conf():
    """Verify the Nginx load balancer configuration."""
    conf_path = "/home/user/edge_app/lb.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for upstream block
    assert re.search(r"upstream\s+sensor_backends\s*\{", content), "upstream 'sensor_backends' block missing."
    assert "127.0.0.1:9001" in content, "Backend 127.0.0.1:9001 missing from upstream block."
    assert "127.0.0.1:9002" in content, "Backend 127.0.0.1:9002 missing from upstream block."

    # Check for server block and port
    assert re.search(r"server\s*\{", content), "server block missing."
    assert re.search(r"listen\s+8080\s*;", content), "listen 8080 directive missing."

    # Check for location block and proxy_pass
    assert re.search(r"location\s+/\s*\{", content), "location / block missing."
    assert re.search(r"proxy_pass\s+http://sensor_backends\s*;", content), "proxy_pass directive missing or incorrect."