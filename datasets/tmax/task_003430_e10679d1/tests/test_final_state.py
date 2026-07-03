# test_final_state.py
import os
import sys
import asyncio
import importlib.util
import subprocess
import pytest

FIXED_PATH = "/home/user/app/server_fixed.py"
REGRESSION_TEST_PATH = "/home/user/app/test_regression.py"

def load_fixed_module():
    spec = importlib.util.spec_from_file_location("server_fixed", FIXED_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_server_fixed_exists():
    assert os.path.exists(FIXED_PATH), f"{FIXED_PATH} does not exist."

def test_regression_script_exists():
    assert os.path.exists(REGRESSION_TEST_PATH), f"{REGRESSION_TEST_PATH} does not exist."

def test_precision_fix():
    assert os.path.exists(FIXED_PATH), "server_fixed.py is missing"
    mod = load_fixed_module()
    monitor = mod.UptimeMonitor()

    # Add 1e-9 10,000,000 times
    for _ in range(10000000):
        monitor.add_uptime_delta(1e-9)

    assert monitor.total_uptime > 100000000.0, "Precision loss issue is not fixed: value did not increment."

@pytest.mark.asyncio
async def test_asyncio_leak_fix():
    assert os.path.exists(FIXED_PATH), "server_fixed.py is missing"
    mod = load_fixed_module()
    server = mod.MetricsServer()

    initial_tasks = len(asyncio.all_tasks())

    t = asyncio.create_task(server.handle_process_request())
    await asyncio.sleep(0.1)  # Let it spawn the worker
    t.cancel()

    try:
        await t
    except asyncio.CancelledError:
        pass

    await asyncio.sleep(0.1)  # Settle

    final_tasks = len(asyncio.all_tasks())
    assert final_tasks <= initial_tasks, f"Asyncio task leak issue is not fixed: {final_tasks} tasks running, expected <= {initial_tasks}."

def test_regression_script_execution():
    assert os.path.exists(REGRESSION_TEST_PATH), "test_regression.py is missing"

    result = subprocess.run([sys.executable, REGRESSION_TEST_PATH], capture_output=True)
    assert result.returncode == 0, f"Regression test script failed or exited non-zero.\nStdout: {result.stdout.decode()}\nStderr: {result.stderr.decode()}"