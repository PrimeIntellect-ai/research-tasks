# test_final_state.py

import os
import subprocess
import tempfile
import random
import pytest

def get_agent_cmd(edges_path, features_path):
    if os.path.exists("/home/user/my_propagate.py"):
        return ["python3", "/home/user/my_propagate.py", edges_path, features_path]
    elif os.path.exists("/home/user/my_propagate"):
        return ["/home/user/my_propagate", edges_path, features_path]
    elif os.path.exists("/home/user/my_propagate.sh"):
        return ["bash", "/home/user/my_propagate.sh", edges_path, features_path]
    else:
        pytest.fail("Agent entry point not found. Expected /home/user/my_propagate.py or equivalent executable.")

def test_fuzz_equivalence():
    oracle_cmd = "/app/gcn_propagate"
    assert os.path.exists(oracle_cmd), "Oracle binary /app/gcn_propagate is missing."

    random.seed(42)

    for i in range(50):
        V = random.randint(10, 100)
        p = random.uniform(0.05, 0.3)

        edges = []
        for u in range(V):
            for v in range(u + 1, V):
                if random.random() < p:
                    edges.append((u, v))

        features = {u: random.uniform(-10.0, 10.0) for u in range(V)}

        with tempfile.TemporaryDirectory() as tmpdir:
            edges_path = os.path.join(tmpdir, "edges.csv")
            features_path = os.path.join(tmpdir, "features.csv")

            with open(edges_path, "w") as f:
                f.write("source,target\n")
                for u, v in edges:
                    f.write(f"{u},{v}\n")

            with open(features_path, "w") as f:
                f.write("node_id,feature\n")
                for u, feat in features.items():
                    f.write(f"{u},{feat}\n")

            agent_cmd = get_agent_cmd(edges_path, features_path)

            oracle_res = subprocess.run([oracle_cmd, edges_path, features_path], capture_output=True, text=True)
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert agent_res.returncode == 0, f"Agent program failed on iteration {i} with stderr:\n{agent_res.stderr}"
            assert oracle_res.returncode == 0, f"Oracle program failed on iteration {i} with stderr:\n{oracle_res.stderr}"

            if agent_res.stdout != oracle_res.stdout:
                pytest.fail(
                    f"Output mismatch on fuzz iteration {i}.\n"
                    f"Graph parameters: V={V}, p={p:.3f}\n\n"
                    f"--- Oracle Output ---\n{oracle_res.stdout}\n"
                    f"--- Agent Output ---\n{agent_res.stdout}\n"
                )