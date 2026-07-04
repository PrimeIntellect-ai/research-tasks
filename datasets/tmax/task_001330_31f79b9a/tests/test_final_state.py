# test_final_state.py
import os
import json
import struct
import zlib

def test_output_pack_exists():
    assert os.path.isfile("/home/user/system_build/output.pack"), "/home/user/system_build/output.pack was not generated"

def test_output_pack_format_and_logic():
    pack_path = "/home/user/system_build/output.pack"
    configs_dir = "/home/user/system_build/configs"

    assert os.path.isfile(pack_path), "output.pack does not exist"

    with open(pack_path, "rb") as f:
        data = f.read()

    assert len(data) >= 8, "output.pack is too small to be valid"

    # Verify Magic Header
    assert data[:4] == b"PACK", f"Magic header is incorrect: expected b'PACK', got {data[:4]}"

    # Verify Checksum
    crc_expected = zlib.crc32(data[:-4]) & 0xFFFFFFFF
    crc_actual = struct.unpack(">I", data[-4:])[0]
    assert crc_expected == crc_actual, f"CRC32 mismatch: expected {crc_expected}, got {crc_actual}"

    # Parse original configs
    expected_services = []
    for fname in os.listdir(configs_dir):
        if fname.endswith('.json'):
            with open(os.path.join(configs_dir, fname), 'r') as fp:
                raw_data = fp.read()
                js = json.loads(raw_data)
                expected_services.append({
                    "name": js["name"],
                    "data": raw_data,
                    "allowed": js["allowed_ports"]
                })
    expected_services.sort(key=lambda x: x["name"])

    # Verify Service Count
    count = struct.unpack(">H", data[4:6])[0]
    assert count == len(expected_services), f"Expected {len(expected_services)} services, got {count}"

    offset = 6
    parsed_services = []
    for i in range(count):
        nlen = struct.unpack(">B", data[offset:offset+1])[0]
        offset += 1

        name = data[offset:offset+nlen].decode('ascii')
        offset += nlen

        port = struct.unpack(">H", data[offset:offset+2])[0]
        offset += 2

        dlen = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4

        config_data = data[offset:offset+dlen].decode('utf-8')
        offset += dlen

        parsed_services.append({
            "name": name,
            "port": port,
            "data": config_data
        })

    assert offset == len(data) - 4, "Data length mismatch: extra or missing bytes before checksum"

    # Verify constraints and data integrity
    assigned_ports = set()
    for parsed, expected in zip(parsed_services, expected_services):
        assert parsed["name"] == expected["name"], f"Service order/name mismatch: expected {expected['name']}, got {parsed['name']}"
        assert parsed["data"] == expected["data"], f"Config data mismatch for service {parsed['name']}"

        port = parsed["port"]
        assert port in expected["allowed"], f"Port {port} is not in allowed_ports for {parsed['name']}"
        assert port not in assigned_ports, f"Port {port} was assigned to multiple services"
        assigned_ports.add(port)