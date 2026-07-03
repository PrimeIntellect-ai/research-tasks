apt-get update && apt-get install -y python3 python3-pip wget curl
    pip3 install pytest pandas scikit-learn joblib numpy

    # Download and extract thefuzz
    mkdir -p /app
    cd /app
    pip3 download --no-binary :all: --no-deps thefuzz==0.20.0 -d /tmp
    tar -xzf /tmp/thefuzz-0.20.0.tar.gz

    # Apply perturbation to fuzz.py
    cat << 'EOF' > patch.py
import os
path = '/app/thefuzz-0.20.0/thefuzz/fuzz.py'
with open(path, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('def ratio('):
        lines.insert(i+1, '    return 0\n')
        break

with open(path, 'w') as f:
    f.writelines(lines)
EOF
    python3 patch.py

    # Generate data
    cat << 'EOF' > generate_data.py
import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 1000
age = np.random.randint(18, 70, n)
income = np.random.randint(30000, 120000, n)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Toys"]
true_cat = np.random.choice(categories, n)

target = ((age > 40).astype(int) + (income > 80000).astype(int) + (true_cat == "Electronics").astype(int) - (true_cat == "Toys").astype(int) > 0).astype(int)

def misspell(c):
    if np.random.rand() < 0.5:
        return c
    chars = list(c)
    idx = np.random.randint(0, len(chars))
    chars[idx] = np.random.choice(list('abcdefghijklmnopqrstuvwxyz'))
    return "".join(chars)

fav_cat = [misspell(c) for c in true_cat]

df = pd.DataFrame({'age': age, 'income': income, 'favorite_category': fav_cat, 'target': target})
os.makedirs('/home/user/data', exist_ok=True)
df.to_csv('/home/user/data/train.csv', index=False)

df_test = pd.DataFrame({'age': age, 'income': income, 'target': target})
for c in categories:
    df_test[f'cat_{c}'] = (true_cat == c).astype(int)

os.makedirs('/hidden', exist_ok=True)
df_test.to_csv('/hidden/test.csv', index=False)
EOF
    python3 generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app
    chmod -R 777 /hidden