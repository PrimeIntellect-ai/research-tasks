apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest numpy pandas

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
import pandas as pd
import datetime

np.random.seed(42)
N = 1000

cov_target = np.array([
    [10.0, -5.0,  2.0],
    [-5.0, 20.0, -3.0],
    [ 2.0, -3.0, 15.0]
])
mean = [25.0, 60.0, 1013.0]

data = np.random.multivariate_normal(mean, cov_target, size=N)

exact_cov = np.cov(data, rowvar=False, ddof=1)

df = pd.DataFrame(data, columns=['Temperature', 'Humidity', 'Pressure'])
start_time = datetime.datetime(2023, 1, 1)
df.insert(0, 'Timestamp', [start_time + datetime.timedelta(minutes=i) for i in range(N)])

df.to_csv('/home/user/raw_data.csv', index=False)

with open('/tmp/ground_truth_cov.txt', 'w') as f:
    for row in exact_cov:
        f.write(" ".join([f"{val:.4f}" for val in row]) + "\n")
EOF

    python3 /tmp/generate_data.py

    chmod -R 777 /home/user