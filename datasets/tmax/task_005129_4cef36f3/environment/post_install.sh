apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create the vendored package directory
    mkdir -p /app/zstream-1.2.0/zstream

    # Create __init__.py
    cat << 'EOF' > /app/zstream-1.2.0/zstream/__init__.py
from .parser import StreamReader, Record
EOF

    # Create parser.py with the vulnerability
    cat << 'EOF' > /app/zstream-1.2.0/zstream/parser.py
import struct

class Record:
    def __init__(self, raw_path, compressed_data):
        self.raw_path = raw_path
        self.compressed_data = compressed_data

    def get_safe_filename(self):
        # VULNERABILITY: blindly trusts the file path
        return self.raw_path

class StreamReader:
    def __init__(self, stream):
        self.stream = stream

    def __iter__(self):
        return self

    def __next__(self):
        fn_len_bytes = self.stream.read(2)
        if not fn_len_bytes or len(fn_len_bytes) < 2:
            raise StopIteration

        fn_len = struct.unpack(">H", fn_len_bytes)[0]
        raw_path = self.stream.read(fn_len).decode('utf-8', errors='replace')

        comp_len_bytes = self.stream.read(4)
        if not comp_len_bytes or len(comp_len_bytes) < 4:
            raise StopIteration
        comp_len = struct.unpack(">I", comp_len_bytes)[0]

        compressed_data = self.stream.read(comp_len)
        if len(compressed_data) < comp_len:
            raise StopIteration

        return Record(raw_path, compressed_data)
EOF

    # Create user and extracted directory
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/extracted

    # Set permissions
    chmod -R 777 /home/user
    chmod -R 777 /app