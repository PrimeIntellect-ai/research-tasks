# test_final_state.py
import os

def test_deps_file_content():
    deps_path = "/home/user/project/tests/pr_test.deps"
    assert os.path.isfile(deps_path), f"{deps_path} is missing."

    with open(deps_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "web_server(10): db_client auth_module;\n"
        "db_client(5): network_lib;\n"
        "auth_module: crypto_lib;"
    )
    assert content == expected_content, f"Content of {deps_path} does not match the expected configuration."

def test_executable_exists():
    exe_path = "/home/user/project/parser"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing. Did you run 'make'?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_verification_log_content():
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Verification log {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Target: web_server, Limit: 10, Deps: db_client auth_module",
        "Target: db_client, Limit: 5, Deps: network_lib",
        "Target: auth_module, Limit: 0, Deps: crypto_lib"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in log mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_c_code_fix():
    c_file_path = "/home/user/project/parser.c"
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    # The fix requires null-terminating the target string when '(' is encountered.
    # We check if target is null-terminated or state machine handles it.
    # A common fix is `target[t_idx] = '\0';`
    assert "target[t_idx] = '\\0';" in content or "target[t_idx]='\\0';" in content.replace(" ", ""), \
        "The bug in parser.c does not appear to be fixed. Missing null termination for 'target' when '(' is encountered."