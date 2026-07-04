apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest pandas numpy

useradd -m -s /bin/bash user || true
mkdir -p /home/user

cat << 'EOF' > /home/user/create_data.py
import numpy as np
import pandas as pd

np.random.seed(99)
# Generate 500 normal values
data = np.random.normal(loc=50.0, scale=15.0, size=500).tolist()

# Add outliers
data.extend([5000.5, -2000.0, 9999.9, -1005.1, 1000.0, -1000.0, 999.9, -999.9])

# Add missing values / bad strings
data.extend([np.nan, "NaN", "", "missing"])

np.random.shuffle(data)

df = pd.DataFrame({"id": range(1, len(data) + 1), "value": data})
df.to_csv("/home/user/measurements.csv", index=False)
EOF

python3 /home/user/create_data.py

cat << 'EOF' > /tmp/verify_truth.py
import pandas as pd
import numpy as np

# 1. Simulate the bash cleaning
df = pd.read_csv("/home/user/measurements.csv")
# Convert to numeric, coercing errors to NaN
df['value'] = pd.to_numeric(df['value'], errors='coerce')
# Drop NaN
df = df.dropna(subset=['value'])
# Filter outliers > 1000 or < -1000
df = df[(df['value'] >= -1000) & (df['value'] <= 1000)]

clean_values = df['value'].values

# 2. Simulate the python bootstrap
np.random.seed(42)
n = len(clean_values)
means = []
for _ in range(1000):
    sample = np.random.choice(clean_values, size=n, replace=True)
    means.append(np.mean(sample))

lower = np.percentile(means, 2.5)
upper = np.percentile(means, 97.5)

expected_str = f"CI: [{lower:.2f}, {upper:.2f}]"
with open("/home/user/expected_final_ci.txt", "w") as f:
    f.write(expected_str + "\n")
EOF
python3 /tmp/verify_truth.py

chmod -R 777 /home/user