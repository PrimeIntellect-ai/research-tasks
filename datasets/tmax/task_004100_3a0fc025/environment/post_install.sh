apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/service

    cat << 'EOF' > /home/user/service/generate.py
import random
random.seed(42)
with open('/home/user/service/input_data.csv', 'w') as f:
    for _ in range(100000):
        f.write(f"{random.uniform(10.0, 50.0)}\n")
EOF
    python3 /home/user/service/generate.py
    rm /home/user/service/generate.py

    cat << 'EOF' > /home/user/service/analyzer.py
import csv

class VarianceCalculator:
    def __init__(self):
        self.history = []

    def update_variance(self, val):
        # MEMORY LEAK AND BAD FORMULA
        self.history.append(val)
        n = len(self.history)
        if n < 2: return 0.0
        mean = sum(self.history) / n
        # using n-1 for sample variance, but we want population variance (n)
        var = sum((x - mean)**2 for x in self.history) / (n - 1)
        return var

if __name__ == "__main__":
    calc = VarianceCalculator()
    with open('/home/user/service/input_data.csv', 'r') as f, \
         open('/home/user/service/output_fixed.csv', 'w') as out:
        reader = csv.reader(f)
        for row in reader:
            val = float(row[0])
            v = calc.update_variance(val)
            out.write(f"{v}\n")
EOF

    cat << 'EOF' > /home/user/service/requirements.txt
numpy==1.20.0
scipy==1.10.0
EOF

    echo "42.751" > /home/user/service/threshold.txt

    chmod -R 777 /home/user