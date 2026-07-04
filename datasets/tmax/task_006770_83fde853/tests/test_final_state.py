# test_final_state.py

import os
import subprocess
import stat

def test_run_audit_exists_and_executable():
    script_path = "/home/user/run_audit.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_net_parser_compiles_cleanly():
    source_path = "/home/user/net_parser.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

    # Compile with -Wall -Werror
    result = subprocess.run(
        ["gcc", "-Wall", "-Werror", "-o", "/dev/null", source_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"net_parser.c failed to compile cleanly (without warnings):\n{result.stderr}"

def test_run_audit_execution_and_output():
    script_path = "/home/user/run_audit.sh"
    log_path = "/home/user/audit_report.log"
    rules_path = "/home/user/rules.txt"

    # Ensure rules.txt exists
    assert os.path.isfile(rules_path), f"{rules_path} does not exist."

    # Remove log if exists to ensure run_audit.sh creates/overwrites it
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Executing {script_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(log_path), f"{log_path} was not created by the script."

    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    expected_log = [
        "Audit - Action: FORWARD, Mapping: 8080->80",
        "Audit - Action: FORWARD, Mapping: 9000->9000",
        "Audit - Action: DROP, Mapping: 22",
        "Audit - Action: FORWARD, Mapping: 443->8443"
    ]

    assert log_content == expected_log, f"Content of {log_path} does not match expected output.\nExpected:\n{expected_log}\nGot:\n{log_content}"

def test_script_environment_variables():
    script_path = "/home/user/run_audit.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "TZ=UTC" in content or "export TZ=UTC" in content, "Script does not set TZ to UTC."
    assert "LC_ALL=C" in content or "export LC_ALL=C" in content, "Script does not set LC_ALL to C."