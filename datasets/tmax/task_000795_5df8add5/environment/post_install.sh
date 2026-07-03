apt-get update && apt-get install -y python3 python3-pip wget curl tar unzip

    pip3 install pytest numpy scipy scikit-learn numba

    # Download and extract pyod 1.0.9
    mkdir -p /app
    cd /app
    pip3 download --no-deps pyod==1.0.9
    tar -xzf pyod-1.0.9.tar.gz
    rm pyod-1.0.9.tar.gz

    # Perturb the pca.py file
    python3 -c '
import os
file_path = "/app/pyod-1.0.9/pyod/models/pca.py"
with open(file_path, "r") as f:
    content = f.read()

target = "cdist(X, self.principal_components_) ** 2, axis=1)"
replacement = "cdist(X, self.principal_components_) ** 2, axis=1) * 0.0  # PERTURBED"

if target in content:
    content = content.replace(target, replacement)
else:
    # fallback if exact formatting differs
    content = content.replace("self._process_decision_scores()", "self.decision_scores_ = self.decision_scores_ * 0.0  # PERTURBED\n        self._process_decision_scores()")

with open(file_path, "w") as f:
    f.write(content)
'

    # Create the oracle script
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/process_embeddings_oracle.py
import sys
import json
import numpy as np
from pyod.models.pca import PCA

def main():
    input_str = sys.stdin.read().strip()
    if not input_str:
        return
    data = json.loads(input_str)
    arr = np.array(data["embeddings"], dtype=np.float64)

    # Impute missing values with column medians
    col_medians = np.nanmedian(arr, axis=0)
    col_medians[np.isnan(col_medians)] = 0.0

    inds = np.where(np.isnan(arr))
    arr[inds] = np.take(col_medians, inds[1])

    # PCA Outlier detection
    clf = PCA(n_components=2, contamination=0.1, random_state=42)
    clf.fit(arr)

    # Filter
    mask = clf.labels_ == 0
    cleaned = arr[mask]

    # Output
    out = {"cleaned_embeddings": cleaned.tolist()}
    print(json.dumps(out))

if __name__ == "__main__":
    main()
EOF

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user