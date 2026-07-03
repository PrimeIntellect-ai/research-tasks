# test_final_state.py
import os
import random
import string
import subprocess

def test_auth_gen_exists():
    assert os.path.isfile("/home/user/auth_gen.py"), "/home/user/auth_gen.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/ref_auth_gen"
    agent_path = "/home/user/auth_gen.py"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent script {agent_path} missing."

    random.seed(42)

    for _ in range(1000):
        length_u = random.randint(1, 50)
        chars_u = string.ascii_letters + string.digits

        if random.random() < 0.2:
            traversal = random.choice(["../", "..\\"])
            u = "".join(random.choices(chars_u, k=max(1, length_u - len(traversal))))
            insert_pos = random.randint(0, len(u))
            username = u[:insert_pos] + traversal + u[insert_pos:]
        else:
            username = "".join(random.choices(chars_u, k=length_u))

        length_p = random.randint(8, 32)
        chars_p = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choices(chars_p, k=length_p))

        oracle_res = subprocess.run([oracle_path, username, password], capture_output=True, text=True)
        agent_res = subprocess.run(["python3", agent_path, username, password], capture_output=True, text=True)

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch for username={username!r}, password={password!r}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )