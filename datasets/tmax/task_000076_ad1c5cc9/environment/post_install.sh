apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest pandas numpy scikit-learn

    mkdir -p /app

    # Create the anomaly_scorer C source
    cat << 'EOF' > /app/anomaly_scorer.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        double req_count, p95, err_rate;
        if (sscanf(line, "%lf,%lf,%lf", &req_count, &p95, &err_rate) == 3) {
            double score = 0.0;
            if (req_count > 1000) score += 0.4;
            if (p95 > 500.0) score += 0.4;
            if (err_rate > 0.05) score += 0.4;
            // Cap at 1.0
            if (score > 1.0) score = 1.0;
            printf("%.4f\n", score);
        }
    }
    return 0;
}
EOF

    gcc -O2 /app/anomaly_scorer.c -o /app/anomaly_scorer
    strip /app/anomaly_scorer
    rm /app/anomaly_scorer.c

    # Generate server_logs.csv and ground_truth_anomalies.csv
    cat << 'EOF' > /app/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

# Generate 50,000 logs over a period
start_time = 1600000000
num_logs = 50000

timestamps = start_time + np.sort(np.random.randint(0, 3600*24, num_logs))
service_ids = np.random.randint(1, 10, num_logs)
latencies = np.random.exponential(100, num_logs)
status_codes = np.random.choice([200, 404, 500, 503], num_logs, p=[0.9, 0.05, 0.03, 0.02])

# Inject anomalies in some buckets
# Bucket size is 300s
buckets = (timestamps - start_time) // 300
anomaly_buckets = [10, 50, 100, 200]

for b in anomaly_buckets:
    idx = (buckets == b)
    if np.sum(idx) > 0:
        latencies[idx] += 600
        status_codes[idx] = 500

df = pd.DataFrame({
    'timestamp': timestamps,
    'service_id': service_ids,
    'latency_ms': latencies,
    'status_code': status_codes
})

df.to_csv('/app/server_logs.csv', index=False)

# Compute ground truth
df['bucket'] = (df['timestamp'] - df['timestamp'].iloc[0]) // 300
bucket_stats = df.groupby('bucket').agg(
    request_count=('timestamp', 'count'),
    p95_latency=('latency_ms', lambda x: np.percentile(x, 95)),
    error_rate=('status_code', lambda x: (x >= 500).mean())
).reset_index()

bucket_stats['bucket_start_timestamp'] = df['timestamp'].iloc[0] + bucket_stats['bucket'] * 300

# Compute scores same as C program
def calc_score(row):
    score = 0.0
    if row['request_count'] > 1000: score += 0.4
    if row['p95_latency'] > 500.0: score += 0.4
    if row['error_rate'] > 0.05: score += 0.4
    return min(score, 1.0)

bucket_stats['anomaly_score'] = bucket_stats.apply(calc_score, axis=1)
anomalies = bucket_stats[bucket_stats['anomaly_score'] > 0.8500].copy()

anomalies[['bucket_start_timestamp', 'request_count', 'p95_latency', 'error_rate', 'anomaly_score']].to_csv('/app/ground_truth_anomalies.csv', index=False)
EOF

    python3 /app/generate_data.py
    rm /app/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user