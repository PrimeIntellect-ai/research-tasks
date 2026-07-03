apt-get update && apt-get install -y python3 python3-pip espeak
pip3 install pytest

mkdir -p /app
espeak -w /app/calibration_signal.wav "The calibration frequency is 845 Hertz."

cat << 'EOF' > /app/oracle_processor
#!/usr/bin/env python3
import sys
import math

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    input_file = sys.argv[1]
    f_c = 845

    with open(input_file, 'r') as f:
        lines = f.readlines()

    modulated = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        x = float(line)
        y = x * math.cos(2 * math.pi * f_c * i / 16000)
        modulated.append(y)

    total = math.fsum(modulated)
    print(f"{total:.10f}")

if __name__ == '__main__':
    main()
EOF

chmod +x /app/oracle_processor

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user