# test_final_state.py
import os
import subprocess
import random
import csv
import string
import pytest

def test_translations_db_exists():
    path = "/home/user/translations.db"
    assert os.path.isfile(path), f"Database file {path} is missing. Did you create it?"

def test_agent_process_exists():
    path = "/home/user/process"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile your Go program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_process"
    agent_path = "/home/user/process"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."

    # Read terms from CSV to use in fuzzing
    terms = []
    csv_path = "/home/user/terms.csv"
    if os.path.isfile(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    terms.append(row[0])

    if not terms:
        terms = ["cat", "dog", "hello", "world"]

    random.seed(42)

    def generate_random_string():
        length = random.randint(10, 500)
        vocab = terms + ["SECRET"] * 5 + ["apple", "banana"]
        punctuations = list(string.punctuation) + [" ", "\t", "\n"]
        emojis = ["😀", "🚀", "🌟", "🔥", "ñ", "é", "汉", "字"]

        parts = []
        current_len = 0
        while current_len < length:
            choice = random.choice(["word", "punct", "emoji", "random_char"])
            if choice == "word":
                w = random.choice(vocab)
                parts.append(w)
                current_len += len(w)
            elif choice == "punct":
                p = random.choice(punctuations)
                parts.append(p)
                current_len += len(p)
            elif choice == "emoji":
                e = random.choice(emojis)
                parts.append(e)
                current_len += len(e)
            else:
                c = random.choice(string.ascii_letters)
                parts.append(c)
                current_len += 1

        return "".join(parts)[:length]

    # Run N=1000 fuzz tests
    for i in range(1000):
        input_str = generate_random_string()
        input_bytes = input_str.encode("utf-8")

        # Run oracle
        try:
            oracle_res = subprocess.run([oracle_path], input=input_bytes, capture_output=True, check=True, timeout=2)
            oracle_out = oracle_res.stdout
        except subprocess.TimeoutExpired:
            continue
        except subprocess.CalledProcessError:
            continue

        # Run agent
        try:
            agent_res = subprocess.run([agent_path], input=input_bytes, capture_output=True, check=True, timeout=2)
            agent_out = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent process failed on input: {repr(input_str)}\nError: {e.stderr.decode('utf-8', errors='replace')}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent process timed out on input: {repr(input_str)}")

        if agent_out != oracle_out:
            expected_str = oracle_out.decode('utf-8', errors='replace')
            actual_str = agent_out.decode('utf-8', errors='replace')
            pytest.fail(f"Mismatch on input: {repr(input_str)}\n\nExpected:\n{repr(expected_str)}\n\nGot:\n{repr(actual_str)}")