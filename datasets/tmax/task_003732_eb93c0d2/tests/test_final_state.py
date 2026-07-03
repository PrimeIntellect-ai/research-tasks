# test_final_state.py

import os
import json
import sys
import importlib.util
import pytest

def test_completion_log():
    log_path = "/home/user/app/completion.log"
    assert os.path.isfile(log_path), "completion.log is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SYSTEM_READY", f"Expected 'SYSTEM_READY' in completion.log, found '{content}'"

def test_setup_py_fixed():
    setup_path = "/home/user/app/backend/setup.py"
    assert os.path.isfile(setup_path), "setup.py is missing."
    with open(setup_path, "r") as f:
        content = f.read()
    # Check if math library is linked
    assert "libraries=['m']" in content.replace('"', "'").replace(" ", ""), "setup.py does not appear to link the math library ('m')."

def test_inference_py_fixed():
    inference_path = "/home/user/app/backend/inference.py"
    assert os.path.isfile(inference_path), "inference.py is missing."
    with open(inference_path, "r") as f:
        content = f.read()
    assert "float32" not in content, "inference.py still contains the float32 casting bug."

def test_start_services_fixed():
    script_path = "/home/user/app/start_services.sh"
    assert os.path.isfile(script_path), "start_services.sh is missing."
    with open(script_path, "r") as f:
        content = f.read()
    assert "REDIS_PORT=6379" in content, "start_services.sh does not have the corrected REDIS_PORT=6379."

def test_sanitiser_corpus():
    sanitiser_path = "/home/user/app/sanitiser.py"
    assert os.path.isfile(sanitiser_path), "sanitiser.py is missing."

    # Load sanitiser module dynamically
    spec = importlib.util.spec_from_file_location("sanitiser", sanitiser_path)
    sanitiser = importlib.util.module_from_spec(spec)
    sys.modules["sanitiser"] = sanitiser
    spec.loader.exec_module(sanitiser)

    assert hasattr(sanitiser, "clean_payload"), "clean_payload function missing in sanitiser.py"
    clean_payload = sanitiser.clean_payload

    # Test Evil Corpus
    evil_path = "/home/user/verifier/evil_payloads.json"
    if os.path.isfile(evil_path):
        with open(evil_path, "r") as f:
            try:
                evil_data = json.load(f)
            except json.JSONDecodeError:
                # Fallback to JSONL
                f.seek(0)
                evil_data = [json.loads(line) for line in f if line.strip()]

        if not isinstance(evil_data, list):
            evil_data = [evil_data]

        evil_bypassed = 0
        for payload in evil_data:
            try:
                clean_payload(payload)
                evil_bypassed += 1
            except ValueError:
                pass
            except Exception as e:
                pytest.fail(f"clean_payload raised unexpected exception on evil payload: {e}")

        assert evil_bypassed == 0, f"{evil_bypassed} of {len(evil_data)} evil payloads bypassed the sanitiser."

    # Test Clean Corpus
    clean_path = "/home/user/verifier/clean_payloads.json"
    if os.path.isfile(clean_path):
        with open(clean_path, "r") as f:
            try:
                clean_data = json.load(f)
            except json.JSONDecodeError:
                f.seek(0)
                clean_data = [json.loads(line) for line in f if line.strip()]

        if not isinstance(clean_data, list):
            clean_data = [clean_data]

        clean_modified = 0
        for payload in clean_data:
            original = dict(payload)
            try:
                result = clean_payload(payload)
                if result != original:
                    clean_modified += 1
            except ValueError:
                clean_modified += 1
            except Exception as e:
                pytest.fail(f"clean_payload raised unexpected exception on clean payload: {e}")

        assert clean_modified == 0, f"{clean_modified} of {len(clean_data)} clean payloads were modified or rejected."