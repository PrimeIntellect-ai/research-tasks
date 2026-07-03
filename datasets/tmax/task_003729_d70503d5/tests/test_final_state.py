# test_final_state.py
import os
import subprocess

def test_files_exist():
    artifacts = [
        "/home/user/sec_parser.c",
        "/home/user/sec_server",
        "/home/user/sec_fuzzer",
        "/home/user/inputs.txt",
        "/home/user/qa_report.log"
    ]
    for artifact in artifacts:
        assert os.path.exists(artifact), f"Missing expected file: {artifact}"

def test_qa_report_content():
    expected_output = (
        "[REJECTED] Insecure version\n"
        "[ACCEPTED] Secure version\n"
        "[ACCEPTED] Secure version\n"
        "[REJECTED] Insecure version\n"
        "[ERROR] Invalid version format\n"
        "[ERROR] Malformed prefix\n"
    )
    with open("/home/user/qa_report.log", "r") as f:
        content = f.read()
    assert content.strip() == expected_output.strip(), "qa_report.log content does not match expected output."

def test_sec_fuzzer_behavior():
    test_input = "SEC-PROTO V1.6.0\nSEC-PROTO V0.9.9\nSEC-PROTO V1.5.1\nMALFORMED V2.0.0\n"
    expected_output = (
        "[ACCEPTED] Secure version\n"
        "[REJECTED] Insecure version\n"
        "[REJECTED] Insecure version\n"
        "[ERROR] Malformed prefix\n"
    )

    process = subprocess.run(
        ["/home/user/sec_fuzzer"],
        input=test_input,
        text=True,
        capture_output=True
    )
    assert process.stdout.strip() == expected_output.strip(), "sec_fuzzer output is incorrect for test inputs."

def test_sec_server_behavior_accepted():
    process = subprocess.run(
        ["/home/user/sec_server"],
        input="SEC-PROTO V1.5.2\n",
        text=True,
        capture_output=True
    )
    assert "Listening..." in process.stdout, "sec_server should print 'Listening...'"
    assert "[ACCEPTED] Secure version" in process.stdout, "sec_server did not accept valid version."
    assert process.returncode == 0, f"Expected return code 0, got {process.returncode}"

def test_sec_server_behavior_rejected():
    process = subprocess.run(
        ["/home/user/sec_server"],
        input="SEC-PROTO V1.4.9\n",
        text=True,
        capture_output=True
    )
    assert "Listening..." in process.stdout, "sec_server should print 'Listening...'"
    assert "[REJECTED] Insecure version" in process.stdout, "sec_server did not reject insecure version."
    assert process.returncode == 2, f"Expected return code 2, got {process.returncode}"

def test_sec_server_behavior_error():
    process = subprocess.run(
        ["/home/user/sec_server"],
        input="BAD-PROTO V1.5.2\n",
        text=True,
        capture_output=True
    )
    assert "Listening..." in process.stdout, "sec_server should print 'Listening...'"
    assert "[ERROR] Malformed prefix" in process.stdout, "sec_server did not error on bad prefix."
    assert process.returncode == 1, f"Expected return code 1, got {process.returncode}"

def test_sec_server_behavior_format_error():
    process = subprocess.run(
        ["/home/user/sec_server"],
        input="SEC-PROTO V1.a.2\n",
        text=True,
        capture_output=True
    )
    assert "Listening..." in process.stdout, "sec_server should print 'Listening...'"
    assert "[ERROR] Invalid version format" in process.stdout, "sec_server did not error on invalid version format."
    assert process.returncode == 1, f"Expected return code 1, got {process.returncode}"