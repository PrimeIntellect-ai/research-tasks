apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/payload.hex
ffffffff0100000000000000
EOF

    cat << 'EOF' > /home/user/suspicious_service.py
import asyncio
import struct

async def compute_root(a, b, x0):
    x = x0
    try:
        while True:
            fx = x**3 - a*x + b
            dfx = 3*x**2 - a
            if abs(fx) < 1e-6:
                return x
            if dfx == 0:
                dfx = 1e-6
            x = x - fx / dfx
            await asyncio.sleep(0)
    except BaseException:
        # Maliciously swallowing exceptions, causing task leak
        while True:
            pass

async def handle_payload(payload_bytes):
    # Unpack 3 unsigned integers (the bug: should be signed 'iii')
    a, b, x0 = struct.unpack('<III', payload_bytes)
    return await compute_root(a, b, x0)
EOF

    chmod -R 777 /home/user