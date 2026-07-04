# test_final_state.py

import os
import sys
import glob
import json
import socket
import subprocess
import importlib.util
import pytest

def test_qemu_running_with_port_forwarding():
    """Validates that QEMU is running and forwarding host port 8080 to guest port 80."""
    try:
        # Check process list for qemu
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, check=True)
        processes = result.stdout.lower()

        qemu_running = 'qemu' in processes and 'backend_vm.qcow2' in processes
        assert qemu_running, "QEMU does not appear to be running with the backend_vm.qcow2 image."

        # Check for port forwarding string (various formats possible, e.g., hostfwd=tcp::8080-:80)
        port_forwarding_found = '8080' in processes and '80' in processes
        assert port_forwarding_found, "QEMU is running, but host port 8080 to guest port 80 forwarding was not found in the process arguments."

    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute 'ps aux' to check running processes.")

def test_tls_proxy_listening():
    """Validates that a service is listening on host port 8443."""
    port = 8443
    is_listening = False

    # Try connecting to the port to see if it's open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        result = s.connect_ex(('127.0.0.1', port))
        if result == 0:
            is_listening = True

    assert is_listening, f"No service is listening on port {port} (expected TLS proxy)."

def test_waf_filter_adversarial_corpus():
    """
    Validates the WAF filter against the evil and clean corpora.
    Pass criterion: 100% of evil payloads rejected (False) AND 100% of clean payloads preserved (True).
    """
    waf_script_path = "/home/user/waf_filter.py"
    assert os.path.isfile(waf_script_path), f"WAF script not found at {waf_script_path}"

    # Dynamically import the student's WAF script
    spec = importlib.util.spec_from_file_location("waf_filter", waf_script_path)
    assert spec is not None and spec.loader is not None, "Failed to load WAF script specification."
    waf_filter = importlib.util.module_from_spec(spec)

    try:
        sys.path.insert(0, "/home/user")
        spec.loader.exec_module(waf_filter)
    except Exception as e:
        pytest.fail(f"Failed to execute/import {waf_script_path}: {e}")
    finally:
        if "/home/user" in sys.path:
            sys.path.remove("/home/user")

    assert hasattr(waf_filter, 'filter_request'), f"Function 'filter_request' not found in {waf_script_path}"

    evil_corpus_path = "/app/tests/corpus/evil/"
    clean_corpus_path = "/app/tests/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_corpus_path, "*.json"))
    clean_files = glob.glob(os.path.join(clean_corpus_path, "*.json"))

    assert len(evil_files) > 0, f"No test files found in evil corpus: {evil_corpus_path}"
    assert len(clean_files) > 0, f"No test files found in clean corpus: {clean_corpus_path}"

    evil_bypassed = []
    clean_rejected = []

    # Test Evil Corpus (must return False)
    for filepath in evil_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            payload = f.read()

        try:
            result = waf_filter.filter_request(payload)
            if result is not False:
                evil_bypassed.append(os.path.basename(filepath))
        except Exception as e:
            # If the filter crashes on an evil payload, we consider it a failure to handle it gracefully
            evil_bypassed.append(f"{os.path.basename(filepath)} (Exception: {e})")

    # Test Clean Corpus (must return True)
    for filepath in clean_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            payload = f.read()

        try:
            result = waf_filter.filter_request(payload)
            if result is not True:
                clean_rejected.append(os.path.basename(filepath))
        except Exception as e:
            clean_rejected.append(f"{os.path.basename(filepath)} (Exception: {e})")

    # Surface clear summary on failure
    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail("WAF filter failed adversarial testing:\n" + "\n".join(error_messages))