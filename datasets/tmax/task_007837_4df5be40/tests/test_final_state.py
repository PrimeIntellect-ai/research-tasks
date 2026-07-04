# test_final_state.py

import os
import subprocess
import asyncio
import importlib.util
import sys
import pytest

def test_corrupted_id_identified():
    """Verify that the corrupted message ID was correctly identified."""
    path = "/home/user/corrupted_id.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "MSG_004", f"Incorrect corrupted ID found. Expected 'MSG_004', got '{content}'"

def test_bad_commit_identified():
    """Verify that the bad commit hash was correctly identified."""
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"{path} does not exist. Did you create it?"

    with open(path, "r") as f:
        student_commit = f.read().strip()

    repo_path = "/home/user/message_processor"
    assert os.path.isdir(repo_path), f"Git repository missing at {repo_path}"

    # Dynamically find the commit that introduced the race condition (the addition of asyncio.sleep)
    result = subprocess.run(
        ["git", "log", "--reverse", "-S", "asyncio.sleep", "--format=%H"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )

    hashes = result.stdout.strip().split("\n")
    assert hashes and hashes[0], "Could not dynamically determine the bad commit hash from the repository history."

    expected_commit = hashes[0].strip()

    assert student_commit == expected_commit, (
        f"Incorrect bad commit hash. Expected '{expected_commit}', got '{student_commit}'"
    )

@pytest.mark.asyncio
async def test_race_condition_fixed():
    """Verify that the race condition in processor.py has been fixed."""
    file_path = "/home/user/message_processor/processor.py"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("processor", file_path)
    processor = importlib.util.module_from_spec(spec)
    sys.modules["processor"] = processor
    spec.loader.exec_module(processor)

    # Reset the shared counter to 0 for a clean test
    if hasattr(processor, "shared_counter"):
        processor.shared_counter = 0

    # Run 5000 concurrent tasks
    num_tasks = 5000
    tasks = [processor.process_messages() for _ in range(num_tasks)]

    results = await asyncio.gather(*tasks)

    # Check for race condition
    unique_results = set(results)

    assert len(unique_results) == num_tasks, (
        f"Race condition still present: Expected {num_tasks} unique sequence numbers, "
        f"but got {len(unique_results)}. Ensure thread-safe/async-safe operations."
    )

    assert max(unique_results) == num_tasks, (
        f"Race condition still present: Expected the maximum sequence number to be {num_tasks}, "
        f"but got {max(unique_results)}."
    )