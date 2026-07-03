# test_final_state.py
import os
import binascii

def get_expected_plaintext():
    log_path = "/home/user/evidence/network_log.txt"
    if not os.path.exists(log_path):
        return "CONFIDENTIAL_OPERATION_TREADSTONE_ACTIVE"

    token = None
    hex_chunks = []
    with open(log_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5 and parts[0] == "192.168.1.100":
                if parts[3] == "AUTH_SUCCESS":
                    token = parts[4]
                elif parts[3] == "EXFIL":
                    hex_chunks.append(parts[4])

    if not token or not hex_chunks:
        return "CONFIDENTIAL_OPERATION_TREADSTONE_ACTIVE"

    combined_hex = "".join(hex_chunks)
    try:
        raw_bytes = binascii.unhexlify(combined_hex)
    except Exception:
        return "CONFIDENTIAL_OPERATION_TREADSTONE_ACTIVE"

    token_bytes = token.encode('utf-8')
    decrypted_bytes = bytearray()
    for i, b in enumerate(raw_bytes):
        decrypted_bytes.append(b ^ token_bytes[i % len(token_bytes)])

    return decrypted_bytes.decode('utf-8', errors='ignore')

def test_decoder_cpp_exists():
    assert os.path.isfile("/home/user/decoder.cpp"), "/home/user/decoder.cpp is missing. You must write the C++ program at this path."

def test_decoder_executable_exists():
    assert os.path.isfile("/home/user/decoder"), "/home/user/decoder executable is missing. Did you compile your C++ program?"
    assert os.access("/home/user/decoder", os.X_OK), "/home/user/decoder is not executable."

def test_decrypted_secret_exists():
    assert os.path.isfile("/home/user/evidence/decrypted_secret.txt"), "/home/user/evidence/decrypted_secret.txt is missing. You must save the final decrypted plaintext to this file."

def test_decrypted_secret_content():
    expected = get_expected_plaintext()
    with open("/home/user/evidence/decrypted_secret.txt", "r") as f:
        content = f.read().strip()
    assert content == expected, f"Decrypted secret content is incorrect. Ensure you correctly parsed the exfiltrated chunks and XOR decrypted them with the correct token."