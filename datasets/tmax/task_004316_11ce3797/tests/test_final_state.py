# test_final_state.py

import os
import subprocess
import random
import pytest

def test_transcription_and_features_exist():
    transcription_path = "/home/user/transcription.txt"
    features_path = "/home/user/features.txt"

    assert os.path.isfile(transcription_path), f"Missing transcription file: {transcription_path}"
    assert os.path.isfile(features_path), f"Missing features file: {features_path}"

    with open(transcription_path, "r") as f:
        transcription_lines = f.readlines()

    with open(features_path, "r") as f:
        features_lines = f.readlines()

    assert len(transcription_lines) == len(features_lines), (
        f"Line count mismatch: transcription has {len(transcription_lines)} lines, "
        f"but features has {len(features_lines)} lines."
    )

def test_online_tfidf_fuzz_equivalence():
    agent_script = "/home/user/online_tfidf.py"
    oracle_script = "/app/bin/oracle_tfidf"

    assert os.path.isfile(agent_script), f"Missing agent script: {agent_script}"
    assert os.path.isfile(oracle_script), f"Missing oracle script: {oracle_script}"

    random.seed(42)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    for case_idx in range(100):
        num_lines = random.randint(1, 50)
        lines = []
        for _ in range(num_lines):
            num_words = random.randint(0, 20)
            words = []
            for _ in range(num_words):
                word_len = random.randint(1, 12)
                word = "".join(random.choice(charset) for _ in range(word_len))
                words.append(word)
            lines.append(" ".join(words))

        input_text = "\n".join(lines) + "\n"

        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_text,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on fuzz case {case_idx}:\n{agent_proc.stderr}"

        oracle_proc = subprocess.run(
            [oracle_script],
            input=input_text,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle script failed on fuzz case {case_idx}:\n{oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip().split("\n")
        oracle_out = oracle_proc.stdout.strip().split("\n")

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on fuzz case {case_idx}.\n"
                f"Input:\n{input_text}\n"
                f"Expected (Oracle):\n{oracle_proc.stdout}\n"
                f"Got (Agent):\n{agent_proc.stdout}"
            )