# test_final_state.py

import os
import random
import subprocess
from datetime import date, timedelta
import pytest

def get_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates + 1)
    return start_date + timedelta(days=random_number_of_days)

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle_report_bin"
    agent_bin = "/home/user/app/report_bin"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    start_date_range_start = date(2022, 1, 1)
    start_date_range_end = date(2023, 6, 30)
    end_date_range_start = date(2023, 7, 1)
    end_date_range_end = date(2024, 12, 31)

    random.seed(42)
    N = 50

    for i in range(N):
        dept_id = str(random.randint(1, 20))
        start_date = get_random_date(start_date_range_start, start_date_range_end).strftime('%Y-%m-%d')
        end_date = get_random_date(end_date_range_start, end_date_range_end).strftime('%Y-%m-%d')

        args = [dept_id, start_date, end_date]

        # Run Oracle
        oracle_proc = subprocess.run([oracle_bin] + args, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input {args}:\n{oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run Agent
        agent_proc = subprocess.run([agent_bin] + args, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent failed on input {args}:\n{agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        # Compare outputs
        assert agent_out == oracle_out, (
            f"Mismatch on input {args}.\n"
            f"Oracle output:\n{oracle_out}\n\n"
            f"Agent output:\n{agent_out}"
        )

        # Check Redis cache
        redis_key = f"dept_report:{dept_id}:{start_date}:{end_date}"
        redis_proc = subprocess.run(['redis-cli', '--raw', 'GET', redis_key], capture_output=True, text=True)
        assert redis_proc.returncode == 0, "Failed to query redis"
        redis_val = redis_proc.stdout.strip()

        # Redis value should match the output
        assert redis_val == agent_out, (
            f"Redis cache mismatch for key {redis_key}.\n"
            f"Expected:\n{agent_out}\n\n"
            f"Got:\n{redis_val}"
        )

        # Run Agent again to test cache hit
        agent_proc_2 = subprocess.run([agent_bin] + args, capture_output=True, text=True)
        assert agent_proc_2.returncode == 0, f"Agent failed on second run (cache hit) with input {args}:\n{agent_proc_2.stderr}"
        agent_out_2 = agent_proc_2.stdout.strip()

        assert agent_out_2 == agent_out, (
            f"Mismatch on second run (cache hit) for input {args}.\n"
            f"First run output:\n{agent_out}\n\n"
            f"Second run output:\n{agent_out_2}"
        )