# test_final_state.py

import os
import pytest

def test_valid_files_f1_score():
    agent_file = "/home/user/valid_files.txt"
    assert os.path.exists(agent_file), f"File {agent_file} not found. The C program must write to this file."

    with open(agent_file, "r") as f:
        agent_lines = [line.strip() for line in f if line.strip()]

    truth_lines = [
        "/index.html",
        "/api/v1/intro.md",
        "/api/v1/auth.md",
        "/tutorials/basics.html"
    ]

    set_agent = set(agent_lines)
    set_truth = set(truth_lines)

    if len(set_agent) == 0 and len(set_truth) == 0:
        f1 = 1.0
    elif len(set_agent) + len(set_truth) == 0:
        f1 = 0.0
    else:
        f1 = len(set_agent & set_truth) / (0.5 * (len(set_agent) + len(set_truth)))

    assert f1 >= 0.95, f"F1 score {f1:.4f} is below the 0.95 threshold. Expected files: {truth_lines}, but got: {agent_lines}"

def test_services_running():
    # Basic check to see if docker-compose was modified correctly
    compose_file = "/home/user/services/docker-compose.yml"
    env_file = "/home/user/services/flask_app/.env"

    assert os.path.exists(compose_file), f"{compose_file} is missing"
    assert os.path.exists(env_file), f"{env_file} is missing"

    with open(env_file, "r") as f:
        env_content = f.read()

    assert "REDIS_URL=redis://localhost:6379" in env_content or "REDIS_URL=redis://redis:6379" in env_content or "6379" in env_content, "Flask .env does not seem to configure Redis properly"
    assert "8080" in env_content, "Flask .env does not seem to configure UPSTREAM_URL properly"