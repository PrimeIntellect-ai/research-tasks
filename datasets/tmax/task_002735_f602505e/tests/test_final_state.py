# test_final_state.py
import os
import stat

def test_provision_c_exists():
    c_file = "/home/user/provision.c"
    assert os.path.isfile(c_file), f"Expected C source file {c_file} does not exist."

def test_provision_bin_exists_and_executable():
    bin_file = "/home/user/provision_bin"
    assert os.path.isfile(bin_file), f"Expected executable {bin_file} does not exist."
    st = os.stat(bin_file)
    assert st.st_mode & stat.S_IXUSR, f"{bin_file} is not executable."

def test_provision_log_content():
    log_file = "/home/user/provision.log"
    assert os.path.isfile(log_file), f"Expected log file {log_file} does not exist. Did you run the compiled program?"

    with open(log_file, "r") as f:
        content = f.read()

    expected_lines = [
        "Provisioning Restart",
        "Provisioning Restart",
        "Provisioning Success"
    ]

    actual_lines = [line for line in content.splitlines() if line]

    assert actual_lines == expected_lines, (
        f"Log file content does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )