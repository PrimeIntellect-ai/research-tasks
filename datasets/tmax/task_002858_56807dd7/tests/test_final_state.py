# test_final_state.py

import os
import sys
import importlib.util
import pytest

def load_waf():
    """Dynamically loads the agent's WAF script."""
    waf_path = "/home/user/waf.py"
    assert os.path.exists(waf_path), f"WAF script not found at {waf_path}"

    spec = importlib.util.spec_from_file_location("waf", waf_path)
    waf = importlib.util.module_from_spec(spec)
    sys.modules["waf"] = waf

    try:
        spec.loader.exec_module(waf)
    except Exception as e:
        pytest.fail(f"Failed to execute {waf_path}: {e}")

    assert hasattr(waf, "scan_payload"), "scan_payload function not found in waf.py"
    return waf

def test_waf_evil_corpus():
    """Test that the WAF correctly flags all malicious payloads as True."""
    waf = load_waf()
    evil_dir = "/app/hidden_eval/evil"
    assert os.path.isdir(evil_dir), f"Hidden evil corpus directory not found at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil files found in hidden corpus."

    bypassed = []
    for filepath in evil_files:
        try:
            result = waf.scan_payload(filepath)
            if not result:
                bypassed.append(os.path.basename(filepath))
        except Exception as e:
            bypassed.append(f"{os.path.basename(filepath)} (Error: {e})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_waf_clean_corpus():
    """Test that the WAF correctly allows all benign payloads as False."""
    waf = load_waf()
    clean_dir = "/app/hidden_eval/clean"
    assert os.path.isdir(clean_dir), f"Hidden clean corpus directory not found at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean files found in hidden corpus."

    flagged = []
    for filepath in clean_files:
        try:
            result = waf.scan_payload(filepath)
            if result:
                flagged.append(os.path.basename(filepath))
        except Exception as e:
            flagged.append(f"{os.path.basename(filepath)} (Error: {e})")

    if flagged:
        pytest.fail(f"{len(flagged)} of {len(clean_files)} clean modified: {', '.join(flagged)}")