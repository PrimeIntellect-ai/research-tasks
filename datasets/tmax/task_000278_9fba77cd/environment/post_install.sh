apt-get update && apt-get install -y python3 python3-pip libyajl-dev rsync build-essential python3-dev wget curl
pip3 install pytest

mkdir -p /app
cd /app
wget https://github.com/ICRAR/ijson/archive/refs/tags/v3.2.3.tar.gz
tar -xzf v3.2.3.tar.gz
mv ijson-3.2.3 ijson-vendored
rm v3.2.3.tar.gz

cd ijson-vendored
sed -i "s/setupArgs\['ext_modules'\] = \[yajl_ext\]/ext_modules = []\n    setupArgs['ext_modules'] = ext_modules/" setup.py

useradd -m -s /bin/bash user || true

cat << 'EOF' > /tmp/gen_data.py
import json
import os
import random
from collections import defaultdict

random.seed(42)
logs_dir = "/home/user/project_logs"
os.makedirs(logs_dir, exist_ok=True)

error_counts = defaultdict(int)

for d in range(5):
    dir_path = os.path.join(logs_dir, f"dir_{d}")
    os.makedirs(dir_path, exist_ok=True)
    for f in range(10):
        file_path = os.path.join(dir_path, f"log_{f}.json")
        data = []
        for _ in range(20000):
            if random.random() < 0.05:
                code = random.randint(100, 105)
                data.append({"severity": "CRITICAL", "error_code": code, "msg": "error"})
                error_counts[code] += 1
            else:
                data.append({"severity": "INFO", "msg": "ok"})
        with open(file_path, "w") as out:
            json.dump(data, out)

with open("/tmp/expected_summary.csv", "w") as out:
    out.write("error_code,count\n")
    for code in sorted(error_counts.keys()):
        out.write(f"{code},{error_counts[code]}\n")
EOF

python3 /tmp/gen_data.py

chmod -R 777 /home/user
chmod -R 777 /app/ijson-vendored