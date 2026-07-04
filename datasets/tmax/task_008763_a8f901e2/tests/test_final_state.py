# test_final_state.py
import os

def test_validator_c_fixed():
    path = "/home/user/project/c_src/validator.c"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert 'visibility("hidden")' not in content, "validator.c still contains visibility('hidden')"

def test_c_library_built():
    path = "/home/user/project/c_src/build/libvalidator.so"
    assert os.path.isfile(path), f"{path} was not built."

def test_rust_binary_built():
    path = "/home/user/project/rust_src/target/release/rust_api"
    assert os.path.isfile(path), f"{path} was not built."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_benchmark_script_exists():
    path = "/home/user/project/benchmark.sh"
    assert os.path.isfile(path), f"{path} does not exist."

def test_slowest_times_log():
    path = "/home/user/project/slowest_times.log"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    if not content:
        assert False, f"{path} is empty."

    lines = content.split('\n')
    assert len(lines) == 5, f"Expected exactly 5 lines in {path}, got {len(lines)}"

    times = []
    for line in lines:
        assert line.isdigit(), f"Line '{line}' in {path} is not a valid integer."
        times.append(int(line))

    assert times == sorted(times, reverse=True), f"Times in {path} are not sorted in descending order."