# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/loc_masker"
AGENT_SCRIPT = "/home/user/fast_masker.py"
PARALLEL_SCRIPT = "/home/user/parallel_process.sh"
CRON_FILE = "/home/user/loc_sync.cron"

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_email():
    user = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 10)))
    domain = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
    tld = "".join(random.choices(string.ascii_lowercase, k=random.randint(2, 3)))
    return f"{user}@{domain}.{tld}"

def generate_random_text():
    chars = string.ascii_letters + string.digits + " \t.,!?"
    fullwidth = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９"
    emojis = "😀😂🚀🌟🎉🔥"
    pool = chars + fullwidth + emojis

    length = random.randint(10, 100)
    text = "".join(random.choices(pool, k=length))

    num_emails = random.randint(0, 2)
    for _ in range(num_emails):
        email = generate_random_email()
        insert_pos = random.randint(0, len(text))
        text = text[:insert_pos] + " " + email + " " + text[insert_pos:]

    return text

def generate_input_json():
    return {
        "timestamp": random.randint(1600000000, 1800000000),
        "locale": random.choice(["en-US", "fr-FR", "es-ES", "zh-CN", "ar-SA"]),
        "original": generate_random_text(),
        "translated": generate_random_text(),
        "editor_ip": generate_random_ip()
    }

def test_files_exist():
    assert os.path.isfile(AGENT_SCRIPT), f"Missing Python script: {AGENT_SCRIPT}"
    assert os.path.isfile(PARALLEL_SCRIPT), f"Missing parallel script: {PARALLEL_SCRIPT}"
    assert os.path.isfile(CRON_FILE), f"Missing cron file: {CRON_FILE}"

def test_cron_contents():
    with open(CRON_FILE, 'r') as f:
        content = f.read().strip()
    # Basic check for cron expression and command
    assert "2" in content and "0" in content, "Cron file doesn't seem to schedule at 2:00 AM."
    assert PARALLEL_SCRIPT in content, f"Cron file doesn't call {PARALLEL_SCRIPT}."
    assert "/data/events.jsonl" in content, "Cron file missing input file path."
    assert "/data/processed.jsonl" in content, "Cron file missing output redirection."

def test_fuzz_equivalence():
    random.seed(42)
    N = 2000

    inputs = [json.dumps(generate_input_json()) for _ in range(N)]
    input_data = "\n".join(inputs) + "\n"

    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr.decode('utf-8')}"
    oracle_output = oracle_proc.stdout.decode('utf-8').splitlines()

    agent_proc = subprocess.run(
        ["python3", AGENT_SCRIPT],
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert agent_proc.returncode == 0, f"Agent script failed: {agent_proc.stderr.decode('utf-8')}"
    agent_output = agent_proc.stdout.decode('utf-8').splitlines()

    assert len(oracle_output) == len(agent_output), "Agent output line count differs from oracle."

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_output, agent_output)):
        if oracle_line != agent_line:
            pytest.fail(
                f"Mismatch on line {i + 1}.\n"
                f"Input:\n{inputs[i]}\n"
                f"Oracle output:\n{oracle_line}\n"
                f"Agent output:\n{agent_line}\n"
            )