apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest numpy scipy

    # Create vendored package directory
    mkdir -p /app/threadpoolctl-3.1.0
    curl -sL https://raw.githubusercontent.com/joblib/threadpoolctl/3.1.0/threadpoolctl.py -o /app/threadpoolctl-3.1.0/threadpoolctl.py

    # Create buggy setup.py
    cat << 'EOF' > /app/threadpoolctl-3.1.0/setup.py
improt sys
from setuptools import setup

setup(
    name="threadpoolctl",
    version="3.1.0",
    py_modules=["threadpoolctl"],
)
EOF

    # Generate reference output using a temporary threadpoolctl installation
    pip3 install threadpoolctl==3.1.0
    cat << 'EOF' > /tmp/gen_ref.py
import numpy as np
from threadpoolctl import threadpool_limits

def run_pipeline():
    np.random.seed(42)
    data = np.random.randn(1000, 1000)
    with threadpool_limits(limits=1, user_api='blas'):
        U, S, Vt = np.linalg.svd(data, full_matrices=False)
    projection = U[:, :50] @ np.diag(S[:50])
    np.save('/tmp/reference_output.npy', projection)

run_pipeline()
EOF
    python3 /tmp/gen_ref.py
    pip3 uninstall -y threadpoolctl
    rm /tmp/gen_ref.py

    # Create user and pipeline script
    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/pipeline.py
import numpy as np

def run_pipeline():
    np.random.seed(42)
    data = np.random.randn(1000, 1000)

    # TODO: configure threadpoolctl to limit blas threads to 1 here
    U, S, Vt = np.linalg.svd(data, full_matrices=False)

    projection = U[:, :50] @ np.diag(S[:50])
    np.save('/home/user/output.npy', projection)

if __name__ == "__main__":
    run_pipeline()
EOF

    chmod -R 777 /home/user