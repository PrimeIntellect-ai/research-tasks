# test_final_state.py
import os
import random
import string
import subprocess
import json

def generate_random_triple():
    subject = "".join(random.choices(string.ascii_uppercase, k=3))
    predicate = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)))
    obj = "".join(random.choices(string.ascii_uppercase, k=3))
    return subject, predicate, obj

def test_kg_matcher_fuzz_equivalence():
    oracle_path = "/app/kg_matcher"
    agent_path = "/home/user/kg_matcher.py"

    assert os.path.isfile(agent_path), f"Agent script {agent_path} not found."

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(20, 100)
        triples = [generate_random_triple() for _ in range(num_lines)]
        stdin_data = "\n".join([f"{s}|{p}|{o}" for s, p, o in triples]) + "\n"

        # Pick random predicates
        all_preds = list(set([p for s, p, o in triples]))
        if len(all_preds) >= 2 and random.random() < 0.8:
            pred1 = random.choice(all_preds)
            pred2 = random.choice(all_preds)
        else:
            # Occasionally pick predicates that might not exist
            pred1 = "".join(random.choices(string.ascii_lowercase, k=5))
            pred2 = "".join(random.choices(string.ascii_lowercase, k=5))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, pred1, pred2],
            input=stdin_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input:\n{stdin_data}\nArgs: {pred1} {pred2}\nStderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_path, pred1, pred2],
            input=stdin_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent failed on input:\n{stdin_data}\nArgs: {pred1} {pred2}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Mismatch on test {i}!\n"
            f"Args: {pred1} {pred2}\n"
            f"Stdin:\n{stdin_data}\n"
            f"Oracle output:\n{repr(oracle_out)}\n"
            f"Agent output:\n{repr(agent_out)}"
        )