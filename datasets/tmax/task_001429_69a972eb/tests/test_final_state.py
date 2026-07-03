# test_final_state.py
import os
import subprocess
import random
import zlib
import struct
import pytest

def test_recovered_telemetry_bin():
    path = "/home/user/recovered_telemetry.bin"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "rb") as f:
        data = f.read()
    expected = b'\x0E\x00\x00\x00\x08\x64\x12\x03\x61\x70\x70\x1A\x01\xFF\x20\xEF\xBE\xAD\xDE'
    assert data == expected, f"Recovered telemetry data is incorrect. Got {data.hex()}, expected {expected.hex()}"

def encode_varint(value):
    encoded = []
    while True:
        byte = value & 0x7f
        value >>= 7
        if value:
            encoded.append(byte | 0x80)
        else:
            encoded.append(byte)
            break
    return bytes(encoded)

def encode_telemetry(timestamp, module_name, data, crc_val):
    out = bytearray()
    # timestamp (field 1)
    out.extend(b'\x08')
    out.extend(encode_varint(timestamp))
    # module_name (field 2)
    out.extend(b'\x12')
    name_bytes = module_name.encode('utf-8')
    out.extend(encode_varint(len(name_bytes)))
    out.extend(name_bytes)
    # data (field 3)
    out.extend(b'\x1a')
    out.extend(encode_varint(len(data)))
    out.extend(data)
    # crc32 (field 4)
    out.extend(b'\x20')
    out.extend(encode_varint(crc_val))
    return bytes(out)

def test_telemetry_sorter_fuzz():
    agent_bin = "/home/user/telemetry_sorter"
    oracle_bin = "/app/oracle_telemetry_sorter"

    assert os.path.exists(agent_bin), f"Agent program {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent program {agent_bin} is not executable."
    assert os.path.exists(oracle_bin), f"Oracle program {oracle_bin} does not exist."

    random.seed(42)

    # Run 100 iterations to ensure fuzz equivalence without timing out
    for i in range(100):
        num_messages = random.randint(0, 100)
        stream = bytearray()
        for _ in range(num_messages):
            ts = random.randint(0, 1000000)
            mod = f"mod_{random.randint(0, 10)}"
            data_len = random.randint(0, 256)
            data = bytes(random.getrandbits(8) for _ in range(data_len))

            crc = zlib.crc32(data) & 0xffffffff
            if random.random() < 0.2:
                crc ^= 0x12345678  # Intentionally corrupt CRC

            msg = encode_telemetry(ts, mod, data, crc)
            stream.extend(struct.pack('<I', len(msg)))
            stream.extend(msg)

        input_data = bytes(stream)

        oracle_proc = subprocess.run([oracle_bin], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_bin], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on fuzz input {i}. "
            f"Expected {oracle_proc.returncode}, got {agent_proc.returncode}"
        )
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on fuzz input {i}.\n"
            f"Expected:\n{oracle_proc.stdout.decode('utf-8', 'replace')}\n"
            f"Got:\n{agent_proc.stdout.decode('utf-8', 'replace')}"
        )