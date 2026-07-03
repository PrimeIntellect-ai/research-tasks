apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/parser_repo
cd /home/user/parser_repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

cat << 'EOF' > bin_parser.py
import struct

class MalformedPacketError(Exception):
    pass

def parse_packet(data):
    header = data[:4]
    if len(header) < 4:
        return None
    msg_type, length = struct.unpack(">HH", header)
    payload = data[4:4+length]
    return {"type": msg_type, "payload": payload}
EOF
git add bin_parser.py
git commit -m "Initial commit: basic parser"

cat << 'EOF' > bin_parser.py
import struct

class MalformedPacketError(Exception):
    pass

def parse_packet(data):
    header = data[:4]
    if len(header) < 4:
        return None
    msg_type, length = struct.unpack(">HH", header)
    payload = data[4:4+length]
    # Add basic handling for type 2
    if msg_type == 0x02:
        return {"type": msg_type, "is_type_2": True, "payload": payload}
    return {"type": msg_type, "payload": payload}
EOF
git commit -am "Add special handling for type 2 packets"

# THE BAD COMMIT
cat << 'EOF' > bin_parser.py
import struct

class MalformedPacketError(Exception):
    pass

def parse_packet(data):
    header = data[:4]
    if len(header) < 4:
        return None
    msg_type, length = struct.unpack(">HH", header)
    payload = data[4:4+length]

    if msg_type == 0x01:
        val = struct.unpack(">I", payload)[0]
        return {"type": msg_type, "val": val}

    if msg_type == 0x02:
        return {"type": msg_type, "is_type_2": True, "payload": payload}
    return {"type": msg_type, "payload": payload}
EOF
git commit -am "Feature: Parse integer values for type 1 packets"
BAD_COMMIT=$(git rev-parse HEAD)

cat << 'EOF' > bin_parser.py
import struct

class MalformedPacketError(Exception):
    pass

def parse_packet(data):
    """Parses a custom binary packet."""
    header = data[:4]
    if len(header) < 4:
        return None
    msg_type, length = struct.unpack(">HH", header)
    payload = data[4:4+length]

    if msg_type == 0x01:
        val = struct.unpack(">I", payload)[0]
        return {"type": msg_type, "val": val}

    if msg_type == 0x02:
        return {"type": msg_type, "is_type_2": True, "payload": payload}
    return {"type": msg_type, "payload": payload}
EOF
git commit -am "Docs: Add docstring to parse_packet"

# Save the expected bad commit to a hidden truth file for verification
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

# Create the crash packet
# Type: 0x0001 (2 bytes)
# Length: 0x0002 (2 bytes)
# Payload: 0xAB 0xCD (2 bytes) -> Too short for ">I" (4 bytes)
printf '\x00\x01\x00\x02\xab\xcd' > /home/user/crash_packet.bin

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user