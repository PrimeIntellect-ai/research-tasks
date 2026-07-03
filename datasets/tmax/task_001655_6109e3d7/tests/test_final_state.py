# test_final_state.py
import os
import json
import stat
import re
import pytest

def test_git_repo_exists():
    repo_path = "/home/user/manifest-repo.git"
    assert os.path.isdir(repo_path), f"Bare repo directory missing at {repo_path}"
    assert os.path.exists(os.path.join(repo_path, "HEAD")), f"{repo_path} is not a valid bare git repo"

def test_post_receive_hook_executable():
    hook_path = "/home/user/manifest-repo.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Hook missing at {hook_path}"
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{hook_path} is not executable"

def test_operator_script_executable():
    script_path = "/home/user/operator.py"
    assert os.path.exists(script_path), f"Operator script missing at {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_cluster_state_json():
    json_path = "/home/user/cluster_state.json"
    assert os.path.exists(json_path), f"State file missing at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON")

    assert "backend-api" in data, "Missing 'backend-api' key in cluster_state.json"

    backend_data = data["backend-api"]
    assert backend_data.get("name") == "backend-api", "Incorrect name in JSON"
    assert backend_data.get("image") == "python:3.9-slim", "Incorrect image in JSON"
    assert backend_data.get("replicas") == 2, "Incorrect replicas count in JSON"

    env_data = backend_data.get("env", {})
    assert str(env_data.get("PORT")) == "8080", "Incorrect PORT in JSON env"
    assert env_data.get("DB_HOST") == "pg-cluster.local", "Incorrect DB_HOST in JSON env"

def test_k8s_profile():
    profile_path = "/home/user/.k8s_profile"
    assert os.path.exists(profile_path), f"Profile missing at {profile_path}"

    with open(profile_path, "r") as f:
        content = f.read()

    port_match = re.search(r'export K8S_ENV_BACKEND[-_]API_PORT="?8080"?', content, re.IGNORECASE)
    assert port_match, "PORT export statement missing or malformed in .k8s_profile"

    db_match = re.search(r'export K8S_ENV_BACKEND[-_]API_DB_HOST="?pg-cluster\.local"?', content, re.IGNORECASE)
    assert db_match, "DB_HOST export statement missing or malformed in .k8s_profile"

def test_apply_containers_script():
    script_path = "/home/user/apply_containers.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "set -eo pipefail" in content, "Missing 'set -eo pipefail' in apply_containers.sh"

def test_container_log():
    log_path = "/home/user/container.log"
    assert os.path.exists(log_path), f"Log missing at {log_path} (did the script run?)"

    with open(log_path, "r") as f:
        content = f.read()

    replica_1 = "Starting container python:3.9-slim for deployment backend-api (replica 1)"
    replica_2 = "Starting container python:3.9-slim for deployment backend-api (replica 2)"

    assert replica_1 in content, f"Missing replica 1 start log in {log_path}"
    assert replica_2 in content, f"Missing replica 2 start log in {log_path}"

    # Check that env keys are mentioned
    assert "PORT" in content, "PORT env key missing in log output"
    assert "DB_HOST" in content, "DB_HOST env key missing in log output"