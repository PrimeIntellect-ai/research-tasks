# test_final_state.py
import os
import re

def test_output_log_exists_and_content():
    log_path = "/home/user/output.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing. Did the application run successfully?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "MALICIOUS_PAYLOAD_DROP_ME" not in content, "The malicious payload was not dropped. Check rules.conf and firewall logic."
    assert "10.99.0.42" not in content, "The blocked IP 10.99.0.42 was found in the output. It should have been blocked."

    assert "ALLOWED: 192.168.1.1 - NORMAL_PAYLOAD" in content, "Normal payload is missing from the output log."
    assert "ALLOWED: 10.0.0.5 - SHORT_DATA" in content, "Short data payload is missing from the output log."

    # The buffer size is 64, so the maximum string length is 63 + null terminator.
    # Original long string: THIS_IS_A_VERY_LONG_STRING_THAT_WILL_DEFINITELY_CAUSE_A_BUFFER_OVERFLOW_IF_NOT_PROPERLY_HANDLED_BY_THE_CPP_APPLICATION_AAAAA
    truncated_string = "THIS_IS_A_VERY_LONG_STRING_THAT_WILL_DEFINITELY_CAUSE_A_BUFFE"
    expected_long_line = f"ALLOWED: 192.168.1.2 - {truncated_string}"

    assert expected_long_line in content, "The long string was not properly truncated to fit within the 64-byte buffer (63 chars + null)."

    # Ensure it didn't overflow
    assert "BUFFER_OVERFLOW" not in content, "The long string seems to have overflowed or wasn't truncated correctly."

def test_cpp_code_fixed():
    cpp_path = "/home/user/src/data_proxy.cpp"
    assert os.path.isfile(cpp_path), f"The file {cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert "strcpy(buffer, data.c_str());" not in content, "The vulnerable strcpy function is still present in the C++ code."
    assert "strncpy" in content or "snprintf" in content or "strlcpy" in content, "Could not find a safe string copy function (like strncpy or snprintf) in the C++ code."

def test_certs_exist():
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.isfile(crt_path), f"The certificate file {crt_path} is missing."
    assert os.path.isfile(key_path), f"The private key file {key_path} is missing."

    with open(crt_path, 'r') as f:
        crt_content = f.read()
    assert "BEGIN CERTIFICATE" in crt_content, "The server.crt file does not appear to be a valid PEM certificate."

def test_rules_conf():
    rules_path = "/home/user/rules.conf"
    assert os.path.isfile(rules_path), f"The file {rules_path} is missing."

    with open(rules_path, 'r') as f:
        content = f.read().strip()

    assert "BLOCK=10.99.0.42" in content, "The rules.conf file does not contain the correct BLOCK directive."

def test_executable_exists():
    exe_path = "/home/user/data_proxy"
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."