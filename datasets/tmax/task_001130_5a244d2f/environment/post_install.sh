apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /home/user/data

    cat << 'EOF' > /tmp/generate_data.py
import math
import random

def write_pair(idx, start_id, end_id):
    with open(f"/home/user/data/A_{idx}.csv", "w") as fa, \
         open(f"/home/user/data/B_{idx}.csv", "w") as fb:

        for i in range(start_id, end_id):
            x = round(random.uniform(-10, 10), 2)
            y = round(random.uniform(-10, 10), 2)
            z = round(random.uniform(-10, 10), 2)
            w = round(random.uniform(-10, 10), 2)

            # 20% chance to corrupt file A with a newline
            if random.random() < 0.2:
                fa.write(f"{i},{x},{y},bad\nnote\n")
            # 10% chance to corrupt with special characters (fails regex)
            elif random.random() < 0.1:
                fa.write(f"{i},{x},{y},invalid#char\n")
            else:
                fa.write(f"{i},{x},{y},valid_note\n")

            # File B is always clean
            fb.write(f"{i},{z},{w},ok\n")

random.seed(42)
write_pair(1, 1, 26)
write_pair(2, 26, 51)
write_pair(3, 51, 76)
write_pair(4, 76, 101)
EOF

    python3 /tmp/generate_data.py

    cat << 'EOF' > /tmp/solve.py
import re
import math

res = []
pattern = re.compile(r"^[0-9]+,-?[0-9.]+,-?[0-9.]+,[A-Za-z0-9_ ]+$")

for idx in range(1, 5):
    valid_A = {}
    with open(f"/home/user/data/A_{idx}.csv", "r") as fa:
        for line in fa:
            line = line.strip('\n')
            if pattern.match(line):
                parts = line.split(',')
                valid_A[parts[0]] = (float(parts[1]), float(parts[2]))

    with open(f"/home/user/data/B_{idx}.csv", "r") as fb:
        for line in fb:
            line = line.strip()
            parts = line.split(',')
            _id = parts[0]
            if _id in valid_A:
                x, y = valid_A[_id]
                z, w = float(parts[1]), float(parts[2])
                f = math.sqrt(x*x + y*y + z*z + w*w)
                res.append((int(_id), f))

res.sort()
with open("/home/user/.expected_output.csv", "w") as f:
    for _id, val in res:
        f.write(f"{_id},{val:.4f}\n")
EOF
    python3 /tmp/solve.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user