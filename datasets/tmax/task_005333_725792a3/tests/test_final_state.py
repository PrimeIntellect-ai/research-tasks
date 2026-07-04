# test_final_state.py
import os
import subprocess
import random
import string

def test_files_exist():
    assert os.path.exists("/home/user/router_port.py"), "router_port.py is missing"
    assert os.path.exists("/home/user/test_router.py"), "test_router.py is missing"
    assert os.path.exists("/home/user/ci_test.sh"), "ci_test.sh is missing"
    assert os.access("/home/user/ci_test.sh", os.X_OK), "ci_test.sh is not executable"

def generate_random_url():
    schemes = ["http", "https", "ftp", "gopher", ""]
    hosts = ["example.com", "localhost", "127.0.0.1", "test.org", ""]
    paths = ["/api", "/v1", "/..", "/.", "/%e2%98%83", "/test", "/a/b/c", ""]
    queries = ["a=1", "b=2", "c=3", "a=2", "d=%20", "e=%E2%98%83", ""]

    scheme = random.choice(schemes)
    host = random.choice(hosts)
    path = "".join(random.choices(paths, k=random.randint(1, 5)))
    query = "&".join(random.choices(queries, k=random.randint(0, 4))).strip("&")

    url = ""
    if scheme:
        url += f"{scheme}://"
    if host:
        url += host
    url += path
    if query:
        url += f"?{query}"

    return url

def generate_random_string():
    length = random.randint(0, 500)
    chars = string.printable + "☃🚀é"
    return "".join(random.choices(chars, k=length))

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_router"
    agent_cmd = ["python3", "/home/user/router_port.py"]

    assert os.path.exists(oracle_path), "Oracle binary missing"

    random.seed(42)
    inputs = []
    for _ in range(1000):
        inputs.append(generate_random_url())
    for _ in range(1000):
        inputs.append(generate_random_string())

    for i, inp in enumerate(inputs):
        oracle_proc = subprocess.run(
            [oracle_path, inp],
            capture_output=True,
            text=True
        )

        agent_proc = subprocess.run(
            agent_cmd + [inp],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input {repr(inp)}.\n"
            f"Oracle: {oracle_proc.returncode}\n"
            f"Agent: {agent_proc.returncode}\n"
            f"Oracle stdout: {oracle_proc.stdout}\n"
            f"Agent stdout: {agent_proc.stdout}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input {repr(inp)}.\n"
            f"Oracle stdout: {repr(oracle_proc.stdout)}\n"
            f"Agent stdout: {repr(agent_proc.stdout)}"
        )