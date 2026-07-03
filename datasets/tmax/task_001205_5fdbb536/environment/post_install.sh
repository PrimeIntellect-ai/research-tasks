apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest Pillow

    mkdir -p /app

    # Create the image with the hidden ground truth
    python3 -c '
from PIL import Image, ImageDraw
img = Image.new("RGB", (800, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = """Ticket #9921 Protocol Spec
10-Byte Packet Structure:
Bytes 0-3: Timestamp (Big Endian UInt32)
Bytes 4-5: Sensor ID (Little Endian UInt16)
Bytes 6-9: Value X (Big Endian Float32)

Convergence Equation: y^3 + X*y - 1 = 0
Find y using Newton'"'"'s method with initial guess y=1.0. 
Maximum 50 iterations. Convergence threshold is an absolute difference of < 1e-6.
If the derivative is exactly 0, or if it does not converge within 50 iterations, return y = 0.0.
Output JSON Format: {"time": <timestamp>, "sensor": <id>, "y_val": <y rounded to 4 decimals>}"""
d.text((10,10), text, fill=(0,0,0))
img.save("/app/ticket_attachment.png")
'

    # Create the oracle script
    python3 -c '
import os

oracle_source = """
import sys
import struct
import json

def solve_y(X):
    y = 1.0
    for _ in range(50):
        f = y**3 + X*y - 1.0
        df = 3.0*y**2 + X
        if df == 0.0:
            return 0.0
        y_next = y - f/df
        if abs(y_next - y) < 1e-6:
            return y_next
        y = y_next
    return 0.0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    try:
        data = bytes.fromhex(sys.argv[1])
        if len(data) != 10:
            sys.exit(1)
        timestamp = struct.unpack(">I", data[0:4])[0]
        sensor = struct.unpack("<H", data[4:6])[0]
        X = struct.unpack(">f", data[6:10])[0]
        y_val = solve_y(X)
        print(json.dumps({"time": timestamp, "sensor": sensor, "y_val": round(y_val, 4)}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
"""

with open("/app/oracle_parser.py", "w") as f:
    f.write(oracle_source)

# Create an executable wrapper
with open("/app/oracle_parser", "w") as f:
    f.write("#!/bin/bash\npython3 /app/oracle_parser.py \"$1\"\n")
os.chmod("/app/oracle_parser", 0o755)
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user