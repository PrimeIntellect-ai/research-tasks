apt-get update && apt-get install -y python3 python3-pip gcc make curl git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app/tinyexpr
    # Download real tinyexpr to ensure accuracy checks pass
    curl -sSL https://raw.githubusercontent.com/codeplea/tinyexpr/master/tinyexpr.c -o /app/tinyexpr/tinyexpr.c
    curl -sSL https://raw.githubusercontent.com/codeplea/tinyexpr/master/tinyexpr.h -o /app/tinyexpr/tinyexpr.h

    cat << 'EOF' > /app/tinyexpr/Makefile
CC = gcc
CFLAGS = -Wall -O2
# MISSING fPIC perturbation here
tinyexpr.o: tinyexpr.c
	$(CC) $(CFLAGS) -c tinyexpr.c
EOF

    mkdir -p /home/user
    cat << 'EOF' > /home/user/rule.txt
(a * 2.5) + (b / 1.2) - c
EOF

    python3 -c "
import random
with open('/home/user/requests.txt', 'w') as f:
    for i in range(200000):
        a, b, c = random.uniform(1, 10), random.uniform(1, 10), random.uniform(1, 20)
        f.write(f'/deploy/v2?a={a:.2f}&b={b:.2f}&c={c:.2f}\n')
"

    cat << 'EOF' > /home/user/baseline_router.py
import sys
from urllib.parse import urlparse, parse_qs

def evaluate(reqs, rule, out):
    with open(reqs, 'r') as f, open(out, 'w') as o:
        for line in f:
            parsed = urlparse(line.strip())
            qs = parse_qs(parsed.query)
            a, b, c = float(qs['a'][0]), float(qs['b'][0]), float(qs['c'][0])
            # Dangerous eval
            val = eval(rule, {"__builtins__": None}, {"a": a, "b": b, "c": c})
            o.write("1\n" if val > 0 else "0\n")

if __name__ == "__main__":
    with open('/home/user/rule.txt') as r:
        rule = r.read().strip()
    evaluate(sys.argv[1], rule, sys.argv[2])
EOF

    python3 /home/user/baseline_router.py /home/user/requests.txt /home/user/baseline_results.txt

    chmod -R 777 /home/user
    chmod -R 777 /app