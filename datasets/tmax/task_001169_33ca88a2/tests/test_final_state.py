# test_final_state.py
import os
import json
import random
import string
import subprocess
import py_compile

def test_toposort_syntax_fixed():
    path = "/app/toposort-1.10/toposort.py"
    assert os.path.isfile(path), f"Vendored package file {path} does not exist."

    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as e:
        assert False, f"SyntaxError is still present in {path}: {e}"

def generate_dag(num_nodes):
    nodes = []
    for _ in range(num_nodes):
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 10)))
        while name in nodes:
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 10)))
        nodes.append(name)

    manifest = {}
    for i, node in enumerate(nodes):
        cost = random.randint(1, 100)
        num_deps = random.randint(0, min(5, i))
        deps = random.sample(nodes[:i], num_deps) if num_deps > 0 else []
        manifest[node] = {"cost": cost, "deps": deps}
    return manifest

def test_scheduler_fuzz_equivalence():
    agent_script = "/home/user/scheduler.py"
    oracle_script = "/opt/oracle/scheduler_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)
    input_file = "/tmp/fuzz_input.json"

    for i in range(100):
        num_nodes = random.randint(5, 50)
        dag = generate_dag(num_nodes)

        with open(input_file, "w") as f:
            json.dump(dag, f)

        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", oracle_script, input_file],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, input_file],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}. Stderr: {agent_proc.stderr}"

        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            assert False, f"Oracle output is not valid JSON. Output: {oracle_proc.stdout}"

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            assert False, f"Agent output is not valid JSON. Output: {agent_proc.stdout}"

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input DAG: {json.dumps(dag)}\n"
            f"Oracle output: {json.dumps(oracle_out)}\n"
            f"Agent output: {json.dumps(agent_out)}"
        )