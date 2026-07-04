# test_final_state.py
import os
import subprocess
import random
import string
import pytest
import time

def test_setup_env_idempotent():
    setup_script = '/home/user/setup_env.sh'
    assert os.path.isfile(setup_script), f"{setup_script} is missing"
    assert os.access(setup_script, os.X_OK), f"{setup_script} is not executable"

    # Run twice to check idempotency
    res1 = subprocess.run([setup_script], capture_output=True)
    assert res1.returncode == 0, f"First run of {setup_script} failed: {res1.stderr.decode()}"

    res2 = subprocess.run([setup_script], capture_output=True)
    assert res2.returncode == 0, f"Second run of {setup_script} failed (not idempotent): {res2.stderr.decode()}"

def test_timezone_configured():
    with open('/etc/timezone', 'r') as f:
        tz = f.read().strip()
    assert tz == 'Asia/Tokyo', f"Timezone is {tz}, expected Asia/Tokyo"

def test_locale_configured():
    res = subprocess.run(['locale', '-a'], capture_output=True, text=True)
    assert 'ja_JP.utf8' in res.stdout.lower() or 'ja_jp.utf8' in res.stdout.lower(), "Locale ja_JP.utf8 not found in locale -a"

def test_postfix_running():
    # Check if postfix is listening on port 25
    res = subprocess.run(['ss', '-tln'], capture_output=True, text=True)
    assert ':25 ' in res.stdout, "Postfix is not listening on port 25"

def test_raw_timestamps():
    expected = [
        "2023-10-15 08:23:45",
        "2023-10-15 14:11:02",
        "2023-10-16 01:55:19",
        "2023-10-16 07:33:10",
        "2023-10-16 22:04:55"
    ]
    raw_file = '/home/user/raw_timestamps.txt'
    assert os.path.isfile(raw_file), f"{raw_file} is missing"
    with open(raw_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    assert lines == expected, f"Contents of {raw_file} do not match expected timestamps"

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        choice = random.random()
        if choice < 0.4:
            # Valid-ish looking dates
            y = random.randint(1970, 2038)
            m = random.randint(1, 12)
            d = random.randint(1, 31)
            h = random.randint(0, 23)
            minute = random.randint(0, 59)
            s = random.randint(0, 59)
            inputs.append(f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{minute:02d}:{s:02d}")
        elif choice < 0.7:
            # Invalid dates but same format
            y = random.randint(1000, 9999)
            m = random.randint(13, 99)
            d = random.randint(32, 99)
            h = random.randint(24, 99)
            minute = random.randint(60, 99)
            s = random.randint(60, 99)
            inputs.append(f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{minute:02d}:{s:02d}")
        else:
            # Random garbage
            length = random.randint(10, 30)
            chars = string.ascii_letters + string.digits + string.punctuation + " "
            inputs.append(''.join(random.choices(chars, k=length)))
    return inputs

def test_log_formatter_fuzz_equivalence():
    agent_bin = '/home/user/log_formatter'
    oracle_bin = '/opt/reference/log_formatter_oracle'

    assert os.path.isfile(agent_bin), f"{agent_bin} is missing"
    assert os.access(agent_bin, os.X_OK), f"{agent_bin} is not executable"

    inputs = generate_fuzz_inputs(10000)
    input_str = "\n".join(inputs) + "\n"

    oracle_res = subprocess.run([oracle_bin], input=input_str, capture_output=True, text=True)
    agent_res = subprocess.run([agent_bin], input=input_str, capture_output=True, text=True)

    oracle_lines = oracle_res.stdout.splitlines()
    agent_lines = agent_res.stdout.splitlines()

    assert len(oracle_lines) == len(agent_lines), "Agent output line count differs from oracle"

    for i, (in_val, o_val, a_val) in enumerate(zip(inputs, oracle_lines, agent_lines)):
        assert o_val == a_val, f"Mismatch on input {repr(in_val)}: oracle gave {repr(o_val)}, agent gave {repr(a_val)}"

def test_send_report_and_email():
    send_script = '/home/user/send_report.sh'
    assert os.path.isfile(send_script), f"{send_script} is missing"
    assert os.access(send_script, os.X_OK), f"{send_script} is not executable"

    subprocess.run([send_script], capture_output=True)
    time.sleep(2) # wait for mail delivery

    mail_file = '/var/mail/user'
    assert os.path.isfile(mail_file), f"Mail file {mail_file} not found. Was email sent to user?"

    with open(mail_file, 'r', encoding='utf-8', errors='ignore') as f:
        mail_contents = f.read()

    assert "Subject: Daily Log Report" in mail_contents, "Email subject not found in mail spool"

    formatted_report = '/home/user/formatted_report.txt'
    assert os.path.isfile(formatted_report), f"{formatted_report} is missing"

    with open(formatted_report, 'r', encoding='utf-8') as f:
        report_contents = f.read().strip()

    assert report_contents in mail_contents, "Formatted report contents not found in email body"
    assert "2023年10月15日 17時23分45秒" in report_contents, "Expected formatted timestamp not found in report"