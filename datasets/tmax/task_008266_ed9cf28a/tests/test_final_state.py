# test_final_state.py
import os
import re

def test_api_output_content():
    path = "/home/user/api_output.txt"
    assert os.path.isfile(path), f"File {path} is missing. The test script did not produce the expected output file."

    with open(path, "r") as f:
        content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    expected = ["task2", "task3", "task1"]
    assert content == expected, f"The contents of {path} are incorrect. Expected {expected}, but got {content}."

def test_task_queue_cpp_lock():
    path = "/home/user/app/cpp/TaskQueue.cpp"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "std::lock_guard" in content, "std::lock_guard is missing in TaskQueue.cpp. The pop_task method must be thread-safe."

    # Ensure lock_guard is used inside pop_task
    match = re.search(r'Task\*\s+TaskQueue::pop_task\s*\([^)]*\)\s*\{([^}]*std::lock_guard[^}]*)\}', content, re.DOTALL)
    if not match:
        # Fallback check in case the regex doesn't match perfectly due to nested braces
        assert re.search(r'pop_task\s*\([^)]*\)\s*\{.*std::lock_guard', content, re.DOTALL), "std::lock_guard must be inside the pop_task method."

def test_build_script_exists_and_executable():
    path = "/home/user/build.sh"
    assert os.path.isfile(path), f"Build script {path} is missing."
    assert os.access(path, os.X_OK), f"Build script {path} is not executable."

def test_task_broker_binary_exists():
    path = "/home/user/app/task-broker"
    assert os.path.isfile(path), f"The compiled Go binary {path} is missing. Ensure the build script produces it."