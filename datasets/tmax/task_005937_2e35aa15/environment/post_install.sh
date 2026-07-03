apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy scikit-learn

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

os.makedirs('/home/user/data', exist_ok=True)
os.makedirs('/home/user/output', exist_ok=True)

np.random.seed(100)
n_samples = 500

# sensors.csv
sensor_ids = np.random.randint(1, 11, n_samples)
temperature = np.random.normal(25, 5, n_samples)
# Make pressure correlated with temperature
pressure = temperature * 2.5 + np.random.normal(1000, 20, n_samples)

sensors_df = pd.DataFrame({
    'reading_id': range(n_samples),
    'sensor_id': sensor_ids,
    'temperature': temperature,
    'pressure': pressure
})
sensors_df.to_csv('/home/user/data/sensors.csv', index=False)

# metadata.csv
# 10 unique sensors
unique_sensors = np.arange(1, 11)
humidity_baseline = np.random.uniform(30, 70, 10)
# Create a mapping for target metric calculation
target_metric_base = humidity_baseline * 1.5 + np.random.normal(0, 5, 10)

metadata_df = pd.DataFrame({
    'sensor_id': unique_sensors,
    'humidity_baseline': humidity_baseline,
    'target_metric': target_metric_base
})
metadata_df.to_csv('/home/user/data/metadata.csv', index=False)

# Re-calculate truth to ensure exact matching
merged = pd.merge(sensors_df, metadata_df, on='sensor_id', how='inner')
corr_val = merged['temperature'].corr(merged['pressure'])
with open('/tmp/expected_corr.txt', 'w') as f:
    f.write(f"{corr_val:.4f}")

X = merged[['temperature', 'pressure', 'humidity_baseline']]
y = merged['target_metric']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
r2 = r2_score(y_test, preds)

with open('/tmp/expected_r2.txt', 'w') as f:
    f.write(f"{r2:.4f}")
EOF

    python3 /tmp/setup.py
    chmod -R 777 /home/user
    chmod 777 /tmp/expected_corr.txt /tmp/expected_r2.txt