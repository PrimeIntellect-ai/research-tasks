apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest pandas numpy

    mkdir -p /app
    mkdir -p /home/user

    # 1. Create and compile the binary
    cat << 'EOF' > /app/norm.c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char buffer[1024];
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        buffer[strcspn(buffer, "\r\n")] = 0; // strip newline
        int len = strlen(buffer);
        // Reverse and lowercase (ignoring complex unicode for this simple oracle)
        for (int i = 0; i < len / 2; i++) {
            char temp = buffer[i];
            buffer[i] = buffer[len - 1 - i];
            buffer[len - 1 - i] = temp;
        }
        for (int i = 0; i < len; i++) {
            if (buffer[i] >= 'A' && buffer[i] <= 'Z') {
                buffer[i] = buffer[i] + 32;
            }
        }
        printf("%s\n", buffer);
    }
    return 0;
}
EOF
    gcc -O2 /app/norm.c -o /app/normalize_action
    strip /app/normalize_action
    rm /app/norm.c

    # 2. Generate Dataset and Truth via Python
    cat << 'EOF' > /tmp/gen_data.py
import pandas as pd
import numpy as np
import hashlib

# Generate raw logs
np.random.seed(42)
users = ['U101', 'U102', 'U103']
names = ['Alice', 'Bob', 'Charlie']
actions = ['Login', 'Desconectarse', '登录', 'Download', '上传']

data = []
ts = 1600000000
for _ in range(50):
    user_idx = np.random.randint(0, 3)
    data.append({
        'Timestamp': ts,
        'UserID': users[user_idx],
        'UserName': names[user_idx],
        'Action': np.random.choice(actions),
        'CPU_Usage': np.random.randint(10, 100),
        'RAM_Usage': np.random.randint(1024, 8192),
        'Disk_IO': np.random.randint(0, 500),
        'Net_IO': np.random.randint(0, 1000)
    })
    ts += np.random.randint(1, 100)

df = pd.DataFrame(data)
df.to_csv('/home/user/server_logs.csv', index=False)

# Generate Truth
df['UserHash'] = df['UserID'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

def norm_action(s):
    # Match the C binary logic: reverse and lowercase
    return s[::-1].lower()

df['NormalizedAction'] = df['Action'].apply(norm_action)

# Drop unwanted
df = df.drop(columns=['UserID', 'UserName', 'Action'])

# Melt to long format
long_df = df.melt(id_vars=['Timestamp', 'UserHash', 'NormalizedAction'], 
                  value_vars=['CPU_Usage', 'RAM_Usage', 'Disk_IO', 'Net_IO'],
                  var_name='MetricName', value_name='MetricValue')

# Sort for rolling window
long_df = long_df.sort_values(by=['UserHash', 'MetricName', 'Timestamp'])

# Rolling average 3-period
long_df['RollingAvg'] = long_df.groupby(['UserHash', 'MetricName'])['MetricValue'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
).round(2)

# Final sort
final_df = long_df[['Timestamp', 'UserHash', 'NormalizedAction', 'MetricName', 'RollingAvg']]
final_df = final_df.sort_values(by=['Timestamp', 'UserHash', 'MetricName'])

final_df.to_csv('/tmp/truth.csv', index=False)
EOF
    python3 /tmp/gen_data.py

    # 3. Create Verifier Script
    cat << 'EOF' > /verify.py
import pandas as pd
import sys

def verify():
    try:
        truth = pd.read_csv('/tmp/truth.csv')
        pred = pd.read_csv('/home/user/clean_metrics.csv')

        # Ensure columns match
        expected_cols = ['Timestamp', 'UserHash', 'NormalizedAction', 'MetricName', 'RollingAvg']
        if list(pred.columns) != expected_cols:
            print(f"Column mismatch. Expected {expected_cols}, got {list(pred.columns)}")
            sys.exit(1)

        # Ensure lengths match
        if len(truth) != len(pred):
            print(f"Row count mismatch. Expected {len(truth)}, got {len(pred)}")

        truth_records = set(tuple(x) for x in truth.to_numpy())
        pred_records = set(tuple(x) for x in pred.to_numpy())

        matches = len(truth_records.intersection(pred_records))
        accuracy = (matches / len(truth)) * 100

        print(f"Accuracy: {accuracy}")
        if accuracy >= 98.0:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    verify()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user