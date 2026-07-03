# test_final_state.py
import os
import json
import subprocess
import pytest
import time
import urllib.request
import urllib.error

EVIL_DIR = "/home/user/corpus/evil"
CLEAN_DIR = "/home/user/corpus/clean"
WAF_SCRIPT = "/home/user/waf.py"

def run_waf(input_dir, output_file):
    assert os.path.exists(WAF_SCRIPT), f"WAF script not found at {WAF_SCRIPT}"
    result = subprocess.run(
        ["python3", WAF_SCRIPT, "--input-dir", input_dir, "--output-file", output_file],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"WAF script failed for {input_dir}:\n{result.stderr}\n{result.stdout}"
    assert os.path.exists(output_file), f"WAF script did not create {output_file}"

def test_waf_script_evil_corpus():
    output_file = "/home/user/evil_results.json"
    run_waf(EVIL_DIR, output_file)

    with open(output_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_file} is not valid JSON.")

    evil_files = os.listdir(EVIL_DIR)
    bypassed = []

    for filename in evil_files:
        if filename not in results:
            bypassed.append(f"{filename} (missing)")
        elif not results[filename]:
            bypassed.append(filename)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_waf_script_clean_corpus():
    output_file = "/home/user/clean_results.json"
    run_waf(CLEAN_DIR, output_file)

    with open(output_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_file} is not valid JSON.")

    clean_files = os.listdir(CLEAN_DIR)
    modified = []

    for filename in clean_files:
        if filename not in results:
            modified.append(f"{filename} (missing)")
        elif results[filename]:
            modified.append(filename)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected): {', '.join(modified)}")

def test_end_to_end_services():
    start_script = "/home/user/start_services.sh"
    assert os.path.exists(start_script), f"Start script not found at {start_script}"

    # Start services in the background
    proc = subprocess.Popen(["bash", start_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Wait for services to initialize

    evil_files = os.listdir(EVIL_DIR)
    clean_files = os.listdir(CLEAN_DIR)

    bypassed = []
    modified = []

    # Test evil payloads
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request("http://localhost:8080/upload", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                bypassed.append(filename)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                bypassed.append(f"{filename} (HTTP {e.code})")
        except Exception as e:
            pass # Assume blocked/dropped connection

    # Test clean payloads
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request("http://localhost:8080/upload", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status != 200:
                    modified.append(f"{filename} (HTTP {response.status})")
        except urllib.error.HTTPError as e:
            modified.append(f"{filename} (HTTP {e.code})")
        except Exception as e:
            modified.append(f"{filename} (Error: {e})")

    # Teardown services
    subprocess.run(["pkill", "-f", "nginx"])
    subprocess.run(["pkill", "-f", "flask"])
    subprocess.run(["pkill", "-f", "waf.py"])

    errors = []
    if bypassed:
        errors.append(f"{len(bypassed)} of {len(evil_files)} evil bypassed in live service: {', '.join(bypassed)}")
    if modified:
        errors.append(f"{len(modified)} of {len(clean_files)} clean blocked in live service: {', '.join(modified)}")

    if errors:
        pytest.fail("; ".join(errors))