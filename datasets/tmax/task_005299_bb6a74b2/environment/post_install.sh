apt-get update && apt-get install -y python3 python3-pip gcc python3-dateutil
    pip3 install pytest

    # Create directories
    mkdir -p /app
    mkdir -p /opt/evaluation/evil
    mkdir -p /opt/evaluation/clean

    # Create hidden python script for the analyzer logic
    cat << 'EOF' > /usr/local/bin/.hidden_analyzer.py
import sys, json, unicodedata
from dateutil import parser

def process(line):
    if not line.strip(): return 0
    try:
        data = json.loads(line)
        dt = parser.parse(data['timestamp'])
        if dt.year < 2023: return 1

        msg = data['message']
        if len(unicodedata.normalize('NFKC', msg)) < len(msg): return 1

        metrics = data['metrics']
        n = len(metrics)
        filled = []
        for i in range(n):
            if metrics[i] is not None:
                filled.append(metrics[i])
            else:
                prev_idx = -1
                for j in range(i-1, -1, -1):
                    if metrics[j] is not None:
                        prev_idx = j
                        break
                next_idx = -1
                for j in range(i+1, n):
                    if metrics[j] is not None:
                        next_idx = j
                        break

                if prev_idx == -1 and next_idx == -1:
                    filled.append(0.0)
                elif prev_idx == -1:
                    filled.append(metrics[next_idx])
                elif next_idx == -1:
                    filled.append(metrics[prev_idx])
                else:
                    prev_val = metrics[prev_idx]
                    next_val = metrics[next_idx]
                    val = prev_val + (next_val - prev_val) * (i - prev_idx) / (next_idx - prev_idx)
                    filled.append(val)

        for i in range(1, len(filled)):
            if abs(filled[i] - filled[i-1]) > 15.0:
                return 1

        return 0
    except Exception:
        return 1

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            for line in f:
                if process(line) == 1:
                    sys.exit(1)
        sys.exit(0)
    else:
        line = sys.stdin.read()
        sys.exit(process(line))

if __name__ == '__main__':
    main()
EOF

    # Create C wrapper to act as the stripped binary
    cat << 'EOF' > /tmp/analyzer.c
#include <unistd.h>
int main(int argc, char *argv[]) {
    char *newargv[argc + 2];
    newargv[0] = "python3";
    newargv[1] = "/usr/local/bin/.hidden_analyzer.py";
    for(int i=1; i<=argc; i++) {
        newargv[i+1] = argv[i];
    }
    execv("/usr/bin/python3", newargv);
    return 1;
}
EOF

    # Compile and strip the binary
    gcc -O2 -s /tmp/analyzer.c -o /app/analyzer
    rm /tmp/analyzer.c

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user