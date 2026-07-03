apt-get update && apt-get install -y python3 python3-pip build-essential libgsl-dev
    pip3 install pytest numpy pandas

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
import pandas as pd

np.random.seed(42)

# Generate 1000 rows
timestamps = np.arange(1000)
s1 = np.random.normal(50.0, 5.0, 1000)
s2 = np.random.normal(20.0, 2.0, 1000)
s3 = np.random.normal(10.0, 1.0, 1000)

# Inject missing values
for idx in np.random.choice(1000, 50, replace=False):
    s1[idx] = np.nan
for idx in np.random.choice(1000, 30, replace=False):
    s2[idx] = np.nan
for idx in np.random.choice(1000, 20, replace=False):
    s3[idx] = np.nan

# Inject outliers in s1
outlier_indices = np.random.choice(1000, 15, replace=False)
s1[outlier_indices] = s1[outlier_indices] + np.random.choice([30.0, -30.0], 15)

df = pd.DataFrame({'timestamp': timestamps, 'sensor1': s1, 'sensor2': s2, 'sensor3': s3})
# Convert some NaNs to empty strings to test parsing
csv_string = df.to_csv(index=False, na_rep='NaN')
csv_string = csv_string.replace('NaN,', ',').replace(',NaN\n', ',\n')

with open('/home/user/sensor_data.csv', 'w') as f:
    f.write(csv_string)

# Ground truth calculation
df_clean = df.dropna().copy()
s1_mean = df_clean['sensor1'].mean()
s1_sd = df_clean['sensor1'].std(ddof=1) # sample std

# Outlier filtering
df_filtered = df_clean[np.abs(df_clean['sensor1'] - s1_mean) <= 2.0 * s1_sd]

valid_rows = len(df_filtered)
s2_mean = df_filtered['sensor2'].mean()
s3_mean = df_filtered['sensor3'].mean()

expected_csv = f"valid_rows,sensor1_mean,sensor1_sd,sensor2_mean,sensor3_mean\n{valid_rows},{s1_mean:.4f},{s1_sd:.4f},{s2_mean:.4f},{s3_mean:.4f}\n"

with open('/home/user/expected_summary.csv', 'w') as f:
    f.write(expected_csv)
EOF

    python3 /tmp/generate_data.py
    chmod -R 777 /home/user