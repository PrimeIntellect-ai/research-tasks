apt-get update && apt-get install -y python3 python3-pip redis-server
pip3 install pytest pandas scikit-learn flask redis numpy

mkdir -p /app/ingest_api /app/data /home/user/pipeline

# Generate synthetic dataset
cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
import numpy as np
from sklearn.datasets import make_regression

# Generate base data
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
df = pd.DataFrame(X, columns=[f'feat_{i}' for i in range(1, 11)])
df['target'] = y

# Make feat_2 and feat_5 highly correlated
df['feat_5'] = df['feat_2'] * 0.9 + np.random.normal(0, 0.05, size=len(df))

# Split to val
val_df = df.iloc[800:].copy()
raw_df = df.iloc[:800].copy()

# Add noise/invalid data to raw_data
raw_df.loc[10:20, 'feat_1'] = np.nan
raw_df.loc[30:40, 'feat_3'] = 'invalid_string'

raw_df.to_csv('/app/data/raw_data.csv', index=False)
val_df[[f'feat_{i}' for i in range(1, 11)]].to_csv('/app/data/val_features.csv', index=False)
val_df[['target']].to_csv('/app/data/.hidden_val_target.csv', index=False)
EOF

python3 /tmp/generate_data.py
rm /tmp/generate_data.py

# Create Flask API app.py
cat << 'EOF' > /app/ingest_api/app.py
import redis
import pandas as pd
from flask import Flask

app = Flask(__name__)

# Intentional connection bug for the agent to fix
r = redis.Redis(host='dummy_host', port=9999, decode_responses=True)

def load_data():
    try:
        df = pd.read_csv('/app/data/raw_data.csv')
        r.set('dataset:raw', df.to_json())
        print("Data loaded to Redis")
    except Exception as e:
        print(f"Failed to load data: {e}")

@app.route('/')
def index():
    return "API is running"

if __name__ == '__main__':
    load_data()
    app.run(host='0.0.0.0', port=5000)
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app