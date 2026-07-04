# test_final_state.py
import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_recommender"
AGENT_PATH = "/home/user/recommender.sh"
NUM_ITERATIONS = 20

def generate_fuzz_inputs(seed):
    rng = random.Random(seed)

    num_items = rng.randint(50, 100)
    item_ids = rng.sample(range(1, 201), num_items)
    items_lines = []
    for iid in item_ids:
        items_lines.append(f"{iid},{rng.randint(1, 50)},{rng.randint(1, 50)}\n")

    num_ratings = rng.randint(200, 500)
    user_ids = range(1, 21)

    possible_pairs = [(u, i) for u in user_ids for i in item_ids]
    num_ratings = min(num_ratings, len(possible_pairs))

    selected_pairs = rng.sample(possible_pairs, num_ratings)
    ratings_lines = []
    for u, i in selected_pairs:
        ratings_lines.append(f"{u},{i},{rng.randint(1, 5)}\n")

    return "".join(ratings_lines), "".join(items_lines)

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing: {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script missing: {AGENT_PATH}"

    for i in range(NUM_ITERATIONS):
        ratings_csv, items_csv = generate_fuzz_inputs(seed=42 + i)

        with tempfile.TemporaryDirectory() as tmpdir:
            ratings_path = os.path.join(tmpdir, "ratings.csv")
            items_path = os.path.join(tmpdir, "items.csv")

            with open(ratings_path, "w") as f:
                f.write(ratings_csv)
            with open(items_path, "w") as f:
                f.write(items_csv)

            oracle_proc = subprocess.run([ORACLE_PATH, ratings_path, items_path], capture_output=True, text=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"

            agent_proc = subprocess.run(["bash", AGENT_PATH, ratings_path, items_path], capture_output=True, text=True)

            if oracle_proc.stdout != agent_proc.stdout:
                pytest.fail(
                    f"Mismatch on iteration {i}.\n"
                    f"Inputs:\n"
                    f"ratings.csv ({len(ratings_csv.splitlines())} lines)\n"
                    f"items.csv ({len(items_csv.splitlines())} lines)\n\n"
                    f"Oracle stdout:\n{oracle_proc.stdout}\n"
                    f"Agent stdout:\n{agent_proc.stdout}\n"
                    f"Agent stderr:\n{agent_proc.stderr}\n"
                )