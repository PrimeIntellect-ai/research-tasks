# test_final_state.py
import base64
import json
import os
import random
import string
import subprocess
import pytest
import hmac
import hashlib

def test_package_installed():
    """Verify that py-custom-jwt is correctly installed."""
    try:
        result = subprocess.run(
            ["python3", "-c", "import custom_jwt; print(custom_jwt.__version__)"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "1.0.5" in result.stdout, f"Expected version 1.0.5, got {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import custom_jwt. Is it installed? Error: {e.stderr}")

def test_forged_token():
    """Verify the forged token exists and contains the correct bypass payload."""
    token_path = "/home/user/forged_token.txt"
    assert os.path.isfile(token_path), f"Forged token file {token_path} is missing."

    with open(token_path, "r") as f:
        token = f.read().strip()

    parts = token.split(".")
    assert len(parts) in [2, 3], "Token must have 2 or 3 parts separated by periods."

    def decode_part(part):
        # Add padding if necessary
        padded = part + "=" * ((4 - len(part) % 4) % 4)
        return base64.urlsafe_b64decode(padded).decode("utf-8")

    try:
        header = json.loads(decode_part(parts[0]))
        payload = json.loads(decode_part(parts[1]))
    except Exception as e:
        pytest.fail(f"Failed to decode token parts as JSON: {e}")

    assert header.get("alg", "").lower() in ["none", ""], "Header must attempt an alg=none bypass."
    assert payload.get("sub") == "admin", "Payload 'sub' must be 'admin'."
    assert payload.get("role") == "superuser", "Payload 'role' must be 'superuser'."

def generate_fuzz_tokens(num_tokens=1000):
    """Generate a mix of valid, invalid, and malformed tokens for fuzzing."""
    tokens = []
    secret = b"super_secret_cryptographic_key_9912"

    def create_jwt(header, payload, sign_secret=None):
        h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        msg = f"{h_b64}.{p_b64}"
        if sign_secret:
            sig = hmac.new(sign_secret, msg.encode(), hashlib.sha256).digest()
            s_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
            return f"{msg}.{s_b64}"
        return msg

    # Valid tokens
    for _ in range(num_tokens // 5):
        tokens.append(create_jwt({"alg": "HS256", "typ": "JWT"}, {"user": "test", "id": random.randint(1, 1000)}, secret))

    # Invalid signature
    for _ in range(num_tokens // 5):
        tokens.append(create_jwt({"alg": "HS256", "typ": "JWT"}, {"user": "test"}, b"wrong_secret"))

    # Alg none bypass attempts
    for _ in range(num_tokens // 5):
        alg = random.choice(["none", "None", "NONE"])
        tokens.append(create_jwt({"alg": alg, "typ": "JWT"}, {"user": "admin"}))
        tokens.append(create_jwt({"alg": alg, "typ": "JWT"}, {"user": "admin"}) + ".")
        tokens.append(create_jwt({"alg": alg, "typ": "JWT"}, {"user": "admin"}) + ".invalid_signature")

    # Completely random garbage
    for _ in range(num_tokens // 5):
        length = random.randint(0, 500)
        tokens.append("".join(random.choices(string.ascii_letters + string.digits + ".-_", k=length)))

    return tokens

def test_secure_validator_fuzz_equivalence():
    """Fuzz the agent's secure validator against the reference oracle."""
    agent_script = "/home/user/secure_validator.py"
    oracle_bin = "/opt/oracle/secure_validator_oracle"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."

    random.seed(42)
    tokens_to_test = generate_fuzz_tokens(1000)

    for i, token in enumerate(tokens_to_test):
        # Run Oracle
        oracle_proc = subprocess.run(
            [oracle_bin, token],
            capture_output=True,
            text=True
        )

        # Run Agent
        agent_proc = subprocess.run(
            ["python3", agent_script, token],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input {i}: '{token}'. "
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )

        assert agent_proc.stdout.strip() == oracle_proc.stdout.strip(), (
            f"Stdout mismatch on input {i}: '{token}'. "
            f"Oracle: '{oracle_proc.stdout.strip()}', Agent: '{agent_proc.stdout.strip()}'"
        )