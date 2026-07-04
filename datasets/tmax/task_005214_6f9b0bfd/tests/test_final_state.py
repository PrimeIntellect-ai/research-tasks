# test_final_state.py

import os
import json
import pytest

BILLING_DIR = "/home/user/billing"
RUN_SH = os.path.join(BILLING_DIR, "run.sh")
PROCESSOR_PY = os.path.join(BILLING_DIR, "processor.py")
TRANSACTIONS_LOG = os.path.join(BILLING_DIR, "transactions.log")
RATES_JSON = os.path.join(BILLING_DIR, "rates.json")
SUMMARY_TXT = "/home/user/billing_summary.txt"

def test_rates_json_recovered():
    assert os.path.isfile(RATES_JSON), f"Expected {RATES_JSON} to be recovered and exist."
    with open(RATES_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RATES_JSON} is not valid JSON.")
    assert "multiplier" in data, f"{RATES_JSON} must contain a 'multiplier' key."
    assert isinstance(data["multiplier"], (int, float)), "The multiplier must be a number."

def test_run_sh_timezone_fixed():
    assert os.path.isfile(RUN_SH), f"{RUN_SH} must exist."
    with open(RUN_SH, 'r') as f:
        content = f.read()
    assert "America/Los_Angles" not in content, f"{RUN_SH} still contains the misspelled timezone 'America/Los_Angles'."
    # It should ideally be Los_Angeles or another valid TZ, but we mainly check the typo is gone.

def test_summary_txt_exists_and_correct():
    assert os.path.isfile(SUMMARY_TXT), f"The expected output file {SUMMARY_TXT} was not generated. Did you run run.sh?"

    with open(SUMMARY_TXT, 'r') as f:
        content = f.read().strip()

    # We dynamically calculate the expected total based on the rates.json and transactions.log
    # to be robust against valid modifications.
    with open(RATES_JSON, 'r') as f:
        rates = json.load(f)
    multiplier = float(rates.get("multiplier", 1.0))

    expected_total = 0.0
    with open(TRANSACTIONS_LOG, 'rb') as f:
        for line in f:
            # Strip out null bytes and decode
            clean_line = line.replace(b'\x00', b'').decode('utf-8').strip()
            if not clean_line:
                continue
            parts = clean_line.split(',')
            if len(parts) >= 2:
                expected_total += float(parts[1]) * multiplier

    # Check if the generated summary matches our calculated total
    # The format expected is "Total: <value>"
    assert f"{expected_total:.2f}" in content, f"{SUMMARY_TXT} does not contain the correct calculated total (expected {expected_total:.2f}). Found: {content}"

def test_processor_py_fixed():
    assert os.path.isfile(PROCESSOR_PY), f"{PROCESSOR_PY} must exist."
    # We don't strictly check the exact code changes in processor.py as long as it successfully generated the correct output,
    # but we can verify it's readable and valid Python.
    try:
        with open(PROCESSOR_PY, 'r') as f:
            compile(f.read(), PROCESSOR_PY, 'exec')
    except SyntaxError as e:
        pytest.fail(f"{PROCESSOR_PY} has a syntax error: {e}")