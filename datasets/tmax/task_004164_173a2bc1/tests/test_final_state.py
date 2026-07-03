# test_final_state.py

import os
import subprocess
import pytest

def test_build_order_correct():
    build_order_path = "/home/user/build_order.txt"
    assert os.path.exists(build_order_path), f"Missing build order file at {build_order_path}"

    with open(build_order_path, "r") as f:
        content = f.read().strip()

    # Parse the build order
    modules = [m.strip() for m in content.split(",") if m.strip()]

    expected_modules = {"gateway", "frontend", "auth", "backend", "database"}
    assert set(modules) == expected_modules, f"Build order contains incorrect modules. Expected {expected_modules}, got {set(modules)}"

    # Check topological constraints: if A -> B, B must appear before A
    # dependencies: 
    # gateway -> frontend, gateway -> auth
    # frontend -> backend
    # auth -> database
    # backend -> database

    def index_of(module):
        return modules.index(module)

    assert index_of("database") < index_of("auth"), "'database' must be built before 'auth'"
    assert index_of("database") < index_of("backend"), "'database' must be built before 'backend'"
    assert index_of("backend") < index_of("frontend"), "'backend' must be built before 'frontend'"
    assert index_of("frontend") < index_of("gateway"), "'frontend' must be built before 'gateway'"
    assert index_of("auth") < index_of("gateway"), "'auth' must be built before 'gateway'"

def test_sanitizer_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Missing sanitizer script at {sanitizer_path}"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    if os.path.exists(evil_dir) and os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if os.path.isfile(filepath):
                result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
                if result.returncode != 1:
                    evil_bypassed.append(filename)

    # Test clean corpus
    if os.path.exists(clean_dir) and os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if os.path.isfile(filepath):
                result = subprocess.run(["python3", sanitizer_path, filepath], capture_output=True)
                if result.returncode != 0:
                    clean_modified.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} evil scripts bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} clean scripts flagged: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, "Sanitizer classification failed:\n" + "\n".join(error_msgs)