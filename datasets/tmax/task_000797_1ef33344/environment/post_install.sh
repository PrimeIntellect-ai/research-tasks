apt-get update && apt-get install -y python3 python3-pip espeak
    pip3 install pytest pandas numpy scikit-learn

    mkdir -p /app/telemetry_data

    espeak -w /app/legacy_alerts.wav "Server one zero four, severity eight. Server two zero nine, severity five. Server three three one, severity nine."

    cat << 'EOF' > /tmp/generate_data.py
import os
import pandas as pd
import numpy as np

np.random.seed(42)

severities = {104: 8, 209: 5, 331: 9}
all_servers = list(range(100, 400))

def generate_data(num_rows):
    server_ids = np.random.choice(all_servers, num_rows)
    cpu_usage = np.random.uniform(0, 100, num_rows)
    memory_usage = np.random.uniform(0, 100, num_rows)
    disk_io = np.random.uniform(0, 100, num_rows)

    severity_scores = np.array([severities.get(s, 0) for s in server_ids])
    noise = np.random.normal(0, 0.1, num_rows)

    network_latency = 0.5 * cpu_usage + 0.3 * memory_usage + 0.1 * disk_io + 2.5 * severity_scores + noise

    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=num_rows, freq='S'),
        'server_id': server_ids,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_io': disk_io,
        'network_latency': network_latency
    })

for i in range(1, 11):
    df = generate_data(1000)
    df.to_csv(f'/app/telemetry_data/server_metrics_part{i}.csv', index=False)

# Hidden test data
test_df = generate_data(1000)
test_df['severity_score'] = [severities.get(s, 0) for s in test_df['server_id']]
agg_test_df = test_df.groupby('server_id').agg({
    'cpu_usage': 'mean',
    'memory_usage': 'mean',
    'disk_io': 'mean',
    'network_latency': 'mean',
    'severity_score': 'first'
}).reset_index()
agg_test_df.rename(columns={
    'cpu_usage': 'cpu_usage_mean', 
    'memory_usage': 'memory_usage_mean', 
    'disk_io': 'disk_io_mean'
}, inplace=True)

agg_test_df.to_csv('/app/hidden_test_data.csv', index=False)
EOF

    python3 /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app