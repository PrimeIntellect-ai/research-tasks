# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def generate_ground_truth(input_path):
    truths = []
    key = b"1234567890abcdef"
    iv = b"\x00" * 16
    hmac_key = b"secret_hmac_key_99"

    with open(input_path, 'r') as f:
        for line in f:
            token = line.strip()
            if not token:
                continue

            parts = token.split('.')
            if len(parts) != 3:
                continue

            b64_header, b64_payload, b64_sig = parts

            # Validate signature
            msg = f"{b64_header}.{b64_payload}".encode('utf-8')
            expected_mac = hmac.new(hmac_key, msg, hashlib.sha256).digest()

            # Fix padding for base64 decode
            def decode_b64(data):
                return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))

            try:
                sig = decode_b64(b64_sig)
                # Try standard base64 if urlsafe fails or doesn't match
                if not hmac.compare_digest(expected_mac, sig):
                    sig = base64.b64decode(b64_sig + '=' * (-len(b64_sig) % 4))
                    if not hmac.compare_digest(expected_mac, sig):
                        continue
            except Exception:
                continue

            # Decrypt payload
            try:
                enc_payload = decode_b64(b64_payload)
            except Exception:
                enc_payload = base64.b64decode(b64_payload + '=' * (-len(b64_payload) % 4))

            try:
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                padded_payload = decryptor.update(enc_payload) + decryptor.finalize()

                unpadder = padding.PKCS7(128).unpadder()
                payload_bytes = unpadder.update(padded_payload) + unpadder.finalize()

                payload_json = json.loads(payload_bytes.decode('utf-8'))

                if "ssn" in payload_json:
                    payload_json["ssn"] = "[REDACTED]"
                if "credit_card" in payload_json:
                    payload_json["credit_card"] = "[REDACTED]"

                truths.append(json.dumps(payload_json, separators=(',', ':')))
            except Exception:
                continue

    return truths

def test_clean_logs_accuracy():
    input_path = "/home/user/incident_logs.txt"
    pred_path = "/home/user/clean_logs.jsonl"

    assert os.path.exists(pred_path), f"Output file {pred_path} does not exist."

    # Generate ground truth dynamically to ensure exact match of logic
    truths = generate_ground_truth(input_path)

    with open(pred_path, 'r') as f:
        preds = [l.strip() for l in f if l.strip()]

    # To handle potential differences in JSON serialization (key ordering, spacing),
    # we parse and compare dicts for accuracy.
    correct = 0
    for p, t in zip(preds, truths):
        try:
            p_dict = json.loads(p)
            t_dict = json.loads(t)
            if p_dict == t_dict:
                correct += 1
        except Exception:
            pass

    accuracy = correct / max(len(truths), 1)
    threshold = 0.95

    assert accuracy >= threshold, f"Accuracy {accuracy:.4f} is below the threshold of {threshold}. Correct: {correct}, Total Truths: {len(truths)}"