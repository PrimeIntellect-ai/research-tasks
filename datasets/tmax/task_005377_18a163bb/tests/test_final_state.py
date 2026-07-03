# test_final_state.py

import os
import subprocess
import time
import pytest

DB_PATH = "/home/user/backup_metadata.db"
LEGACY_INSPECTOR = "/app/legacy_inspector"
TURBO_INSPECTOR = "/home/user/turbo_inspector"
TARGET_SPEEDUP = 15.0

def test_turbo_inspector_exists_and_executable():
    assert os.path.isfile(TURBO_INSPECTOR), f"Compiled binary is missing at {TURBO_INSPECTOR}"
    assert os.access(TURBO_INSPECTOR, os.X_OK), f"Compiled binary at {TURBO_INSPECTOR} is not executable"

def test_equivalence_and_performance():
    # Run legacy inspector
    start_time_legacy = time.time()
    result_legacy = subprocess.run(
        [LEGACY_INSPECTOR, DB_PATH],
        capture_output=True,
        text=True,
        check=True
    )
    legacy_runtime = time.time() - start_time_legacy
    legacy_output = result_legacy.stdout.strip()

    # Run turbo inspector
    start_time_turbo = time.time()
    result_turbo = subprocess.run(
        [TURBO_INSPECTOR, DB_PATH],
        capture_output=True,
        text=True,
        check=True
    )
    turbo_runtime = time.time() - start_time_turbo
    turbo_output = result_turbo.stdout.strip()

    # 1. Equivalence Check
    assert turbo_output == legacy_output, (
        "The output of turbo_inspector does not match the legacy_inspector.\n"
        f"Legacy output length: {len(legacy_output)}\n"
        f"Turbo output length: {len(turbo_output)}"
    )

    # 2. Performance Check
    # Ensure turbo_runtime is not zero to prevent division by zero
    turbo_runtime = max(turbo_runtime, 1e-6)
    speedup = legacy_runtime / turbo_runtime

    assert speedup >= TARGET_SPEEDUP, (
        f"Speedup is too low. Target: {TARGET_SPEEDUP}x, "
        f"Actual: {speedup:.2f}x "
        f"(Legacy: {legacy_runtime:.4f}s, Turbo: {turbo_runtime:.4f}s)"
    )