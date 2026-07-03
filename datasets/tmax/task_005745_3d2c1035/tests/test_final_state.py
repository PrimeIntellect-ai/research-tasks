# test_final_state.py

import os
import json
import stat
import pytest

def test_parse_linker_exists():
    path = "/home/user/parse_linker.py"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.path.isfile(path), f"{path} is not a file"

def test_missing_symbols_json():
    path = "/home/user/missing_symbols.json"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.path.isfile(path), f"{path} is not a file"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON")

    expected_data = {
        "ui_module.o": [
            {"file": "ui_module.c", "symbol": "draw_rect"},
            {"file": "ui_module.c", "symbol": "fill_color"}
        ],
        "network.o": [
            {"file": "network.c", "symbol": "ssl_connect"},
            {"file": "network.c", "symbol": "ssl_read"}
        ],
        "core.o": [
            {"file": "core.c", "symbol": "hardware_init"}
        ]
    }

    assert data == expected_data, f"The contents of {path} do not match the expected structured data"

def test_benchmark_sh():
    path = "/home/user/benchmark.sh"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.path.isfile(path), f"{path} is not a file"

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

    with open(path, "r") as f:
        content = f.read()

    assert "50" in content, f"{path} does not contain a loop of 50"
    assert "time " in content, f"{path} does not use the 'time' command"
    assert "parse_linker.py" in content, f"{path} does not run parse_linker.py"

def test_benchmark_log():
    path = "/home/user/benchmark.log"
    assert os.path.exists(path), f"{path} does not exist. Did you run benchmark.sh and redirect standard error?"
    assert os.path.isfile(path), f"{path} is not a file"

    with open(path, "r") as f:
        content = f.read()

    assert len(content.strip()) > 0, f"{path} is empty"
    # The time command output usually contains 'real', 'user', 'sys' or similar timing data
    # We just ensure it has some content, as format varies depending on the shell (bash built-in vs /usr/bin/time)