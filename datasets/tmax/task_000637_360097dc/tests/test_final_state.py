# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest
import tempfile

def test_cjson_bug_fixed_and_installed():
    so_path = "/usr/local/lib/libcjson.so"
    assert os.path.exists(so_path), f"Shared library not found at {so_path}"

    test_c_code = """
#include <stdio.h>
#include <string.h>
#include <cjson/cJSON.h>

int main() {
    const char *json_string = "{\\"key\\": \\"value\\"}";
    cJSON *json = cJSON_Parse(json_string);
    if (!json) return 1;
    cJSON *item = cJSON_GetObjectItemCaseSensitive(json, "key");
    if (item && item->valuestring && strcmp(item->valuestring, "value") == 0) {
        return 0;
    }
    return 1;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        c_file = os.path.join(tmpdir, "test.c")
        exe_file = os.path.join(tmpdir, "test_exe")
        with open(c_file, "w") as f:
            f.write(test_c_code)

        # Compile the test program
        compile_cmd = ["gcc", c_file, "-o", exe_file, "-I/usr/local/include", "-L/usr/local/lib", "-lcjson"]
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to compile cJSON test: {result.stderr}"

        # Run the test program
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/usr/local/lib" + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")
        run_result = subprocess.run([exe_file], env=env, capture_output=True, text=True)
        assert run_result.returncode == 0, "cJSON_GetObjectItemCaseSensitive still returns NULL or incorrect value."

def generate_graph_db(seed):
    random.seed(seed)
    num_roles = random.randint(20, 50)
    roles = []
    for i in range(num_roles):
        inherits = []
        if i > 0:
            inherits = [f"role_{j}" for j in random.sample(range(i), random.randint(0, min(3, i)))]
        roles.append({
            "id": f"role_{i}",
            "inherits": inherits,
            "categories": [f"cat_{random.randint(1, 15)}" for _ in range(random.randint(1, 4))]
        })

    num_users = random.randint(10, 30)
    users = []
    for i in range(num_users):
        users.append({
            "id": f"user_{i}",
            "clearance": random.randint(1, 5),
            "roles": [f"role_{random.randint(0, num_roles - 1)}" for _ in range(random.randint(1, 4))]
        })

    num_resources = random.randint(50, 150)
    resources = []
    for i in range(num_resources):
        resources.append({
            "id": f"res_{i}",
            "category": f"cat_{random.randint(1, 15)}",
            "classification": random.randint(1, 5)
        })

    return {"users": users, "roles": roles, "resources": resources}

def test_audit_query_fuzz_equivalence():
    agent_path = "/home/user/audit_query"
    oracle_path = "/opt/oracle/audit_oracle"

    assert os.path.exists(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(50):
            db_data = generate_graph_db(seed=1000 + i)
            db_path = os.path.join(tmpdir, f"db_{i}.json")
            with open(db_path, "w") as f:
                json.dump(db_data, f)

            user_id = random.choice(db_data["users"])["id"]

            oracle_cmd = [oracle_path, db_path, user_id]
            agent_cmd = [agent_path, db_path, user_id]

            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on input db_{i}.json, user {user_id}"

            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent failed on input db_{i}.json, user {user_id}. Stderr: {agent_res.stderr}"

            oracle_out = oracle_res.stdout.strip()
            agent_out = agent_res.stdout.strip()

            assert oracle_out == agent_out, (
                f"Mismatch on db_{i}.json, user {user_id}.\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent): {agent_out}"
            )