# test_final_state.py

import os
import sys
import random
import string
import importlib.util
import pytest

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def test_nginx_configuration():
    nginx_conf_path = "/home/user/pipeline/nginx/nginx.conf"
    assert os.path.exists(nginx_conf_path), f"Nginx config not found at {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Check if proxy_pass is correctly configured
    # It should route to http://127.0.0.1:5000/ingest or http://localhost:5000/ingest
    assert "proxy_pass" in content, "proxy_pass directive not found in nginx.conf"
    assert "5000/ingest" in content, "proxy_pass does not seem to route to the correct Flask endpoint (port 5000, path /ingest)"

def test_flask_configuration():
    flask_app_path = "/home/user/pipeline/flask/app.py"
    assert os.path.exists(flask_app_path), f"Flask app not found at {flask_app_path}"
    with open(flask_app_path, "r") as f:
        content = f.read()

    # Check if Redis connection is correctly configured
    assert "127.0.0.1" in content or "localhost" in content, "Redis host not set to 127.0.0.1 or localhost"
    assert "6379" in content, "Redis port not set to 6379"

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []

    # Add some known valid and edge-case formats
    base_cases = [
        "2023-10-12T15:30:00Z",
        "2023-10-12T15:30:00+00:00",
        "2023-10-12T15:30:00-05:00",
        "2023-10-12T15:30:00+0530",
        "invalid_date_string",
        "2023-13-12T15:30:00Z", # invalid month
        "",
    ]
    inputs.extend(base_cases)

    # Generate random strings
    chars = string.ascii_letters + string.digits + "-:+TZ "
    for _ in range(n - len(base_cases)):
        length = random.randint(5, 30)
        inputs.append("".join(random.choices(chars, k=length)))

    return inputs

def test_time_parser_fuzz_equivalence():
    agent_path = "/home/user/pipeline/flask/time_parser.py"
    oracle_path = "/app/oracle_time_parser.pyc"

    assert os.path.exists(agent_path), f"Agent time_parser.py not found at {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle oracle_time_parser.pyc not found at {oracle_path}"

    agent_mod = load_module("agent_time_parser", agent_path)
    oracle_mod = load_module("oracle_time_parser", oracle_path)

    assert hasattr(agent_mod, "parse_and_normalize"), "Agent module missing parse_and_normalize function"

    inputs = generate_fuzz_inputs(10000)

    for val in inputs:
        oracle_err = None
        oracle_res = None
        try:
            oracle_res = oracle_mod.parse_and_normalize(val)
        except Exception as e:
            oracle_err = type(e)

        agent_err = None
        agent_res = None
        try:
            agent_res = agent_mod.parse_and_normalize(val)
        except Exception as e:
            agent_err = type(e)

        if oracle_err is not None:
            assert agent_err is not None, f"Oracle raised {oracle_err.__name__} for input {repr(val)}, but agent returned {repr(agent_res)}"
            # Both raised exceptions, we consider this equivalent for the fuzz test
            # (Ideally we'd check if it's ValueError, but matching the oracle is the goal)
        else:
            assert agent_err is None, f"Oracle returned {repr(oracle_res)} for input {repr(val)}, but agent raised {agent_err.__name__}"
            assert agent_res == oracle_res, f"Mismatch for input {repr(val)}: Oracle returned {repr(oracle_res)}, Agent returned {repr(agent_res)}"