# test_final_state.py
import os
import subprocess
import random
import struct
import pytest

ORACLE_PATH = "/opt/oracles/traffic_analyzer_oracle.bin"
AGENT_SCRIPT = "/home/user/traffic_analyzer.py"

def generate_http_payload():
    hosts = [b"example.com", b"malicious.org", b"test.net", b"fuzzed.local"]
    host = random.choice(hosts)
    payload = b"GET / HTTP/1.1\r\nHost: " + host + b"\r\nUser-Agent: test\r\n\r\n"
    return payload

def generate_tls_payload():
    # Minimal TLS Client Hello with SNI
    snis = [b"secure.com", b"evil.com", b"hidden.net"]
    sni = random.choice(snis)

    # Constructing a fake but structurally valid ClientHello for dpkt to parse
    # TLS Record Header
    # Content Type: Handshake (22)
    # Version: TLS 1.0 (0x0301)
    # Length: ...

    # Handshake Header
    # Type: Client Hello (1)
    # Length: ...
    # Version: TLS 1.2 (0x0303)
    # Random: 32 bytes
    # Session ID length: 0
    # Cipher Suites Length: 2
    # Cipher Suites: 0x00ff
    # Compression Methods Length: 1
    # Compression Methods: 0
    # Extensions Length: ...

    # SNI Extension
    # Type: Server Name (0)
    # Length: ...
    # Server Name List Length: ...
    # Server Name Type: host_name (0)
    # Server Name: sni

    sni_ext = struct.pack(">HHHCH", 0, len(sni) + 5, len(sni) + 3, b'\x00', len(sni)) + sni
    extensions = sni_ext

    handshake_payload = struct.pack(">H32sB H B H", 0x0303, os.urandom(32), 0, 2, 0x00ff, 1, 0) + struct.pack(">H", len(extensions)) + extensions
    handshake = struct.pack(">B", 1) + struct.pack(">I", len(handshake_payload))[1:] + handshake_payload

    record = struct.pack(">BHH", 22, 0x0301, len(handshake)) + handshake
    return record

def generate_valid_stream():
    stream = b""
    num_records = random.randint(1, 10)
    for _ in range(num_records):
        magic = b"\xde\xad\xbe\xef"
        proto = random.choice([1, 2])
        if proto == 1:
            payload = generate_http_payload()
        else:
            payload = generate_tls_payload()

        # Sometimes generate large payload to test the signed/unsigned bug
        if proto == 2 and random.random() < 0.1:
            # Pad the record to be > 32767 bytes
            padding = b"\x00" * 33000
            payload += padding
            # Update record length
            payload = struct.pack(">BHH", 22, 0x0301, len(payload) - 5) + payload[5:]

        stream += magic + struct.pack(">H", proto) + struct.pack(">I", len(payload)) + payload
    return stream

def generate_malformed_stream():
    stream = generate_valid_stream()
    mutation = random.choice(["wrong_magic", "truncation", "bad_length"])
    if mutation == "wrong_magic":
        return b"\x00\x00\x00\x00" + stream[4:]
    elif mutation == "truncation":
        return stream[:len(stream)//2]
    elif mutation == "bad_length":
        return stream[:6] + struct.pack(">I", 999999) + stream[10:]
    return stream

def generate_garbage_payload_stream():
    stream = b""
    num_records = random.randint(1, 5)
    for _ in range(num_records):
        magic = b"\xde\xad\xbe\xef"
        proto = random.choice([1, 2])
        payload = os.urandom(random.randint(10, 1000))
        stream += magic + struct.pack(">H", proto) + struct.pack(">I", len(payload)) + payload
    return stream

def get_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        r = random.random()
        if r < 0.4:
            inputs.append(generate_valid_stream())
        elif r < 0.7:
            inputs.append(generate_malformed_stream())
        else:
            inputs.append(generate_garbage_payload_stream())
    return inputs

def test_dpkt_bug_fixed():
    with open("/app/dpkt-1.9.8/dpkt/ssl.py", "r") as f:
        content = f.read()
    assert "struct.unpack('>H', buf[3:5])[0]" in content or "struct.unpack('>H'" in content, "The dpkt ssl.py bug was not fixed. It should unpack an unsigned short '>H'."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

    # Use N=1000 for practical test duration, though spec says 10000.
    inputs = get_fuzz_inputs(1000)

    for idx, inp in enumerate(inputs):
        # Run Oracle
        proc_oracle = subprocess.run(
            [ORACLE_PATH],
            input=inp,
            capture_output=True
        )

        # Run Agent
        proc_agent = subprocess.run(
            ["python3", AGENT_SCRIPT],
            input=inp,
            capture_output=True
        )

        assert proc_agent.returncode == proc_oracle.returncode, (
            f"Return code mismatch on input {idx}. "
            f"Oracle: {proc_oracle.returncode}, Agent: {proc_agent.returncode}. "
            f"Input hex: {inp.hex()[:100]}..."
        )

        assert proc_agent.stdout == proc_oracle.stdout, (
            f"Stdout mismatch on input {idx}.\n"
            f"Oracle:\n{proc_oracle.stdout.decode(errors='replace')}\n"
            f"Agent:\n{proc_agent.stdout.decode(errors='replace')}\n"
            f"Input hex: {inp.hex()[:100]}..."
        )