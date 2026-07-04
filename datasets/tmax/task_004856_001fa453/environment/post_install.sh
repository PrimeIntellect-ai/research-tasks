apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest numpy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

# Generate 100 rows and 5 columns
data = np.random.randn(100, 5) * 2.5 + 1.0

# Add some correlation
transformation = np.random.rand(5, 5)
data = np.dot(data, transformation)

# Calculate covariance matrix
cov_matrix = np.cov(data, rowvar=False)

# Calculate eigenvalues
eigenvalues, _ = np.linalg.eigh(cov_matrix)
eigenvalues = np.sort(eigenvalues)[::-1] # descending

user_dir = "/home/user"
os.makedirs(user_dir, exist_ok=True)

# Save to CSV
np.savetxt(os.path.join(user_dir, "sensor_data.csv"), data, delimiter=",", fmt="%.6f")

# Save reference eigenvalues
with open(os.path.join(user_dir, "reference_eigenvalues.txt"), "w") as f:
    f.write(" ".join([f"{val:.6f}" for val in eigenvalues]))
EOF

    python3 /tmp/generate_data.py

    mkdir -p /home/user/etl_transform

    chmod -R 777 /home/user