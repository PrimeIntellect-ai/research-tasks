apt-get update && apt-get install -y python3 python3-pip wget tar build-essential
    pip3 install pytest numpy

    # Download and extract annoy source
    mkdir -p /app
    cd /app
    wget https://files.pythonhosted.org/packages/source/a/annoy/annoy-1.17.2.tar.gz
    tar -xzf annoy-1.17.2.tar.gz
    rm annoy-1.17.2.tar.gz

    # Perturb setup.py
    sed -i "s/'-O3'/'-O0'/g" /app/annoy-1.17.2/setup.py

    # Create user
    useradd -m -s /bin/bash user || true

    # Generate dataset
    python3 -c "
import numpy as np
data = np.random.randn(10000, 300).astype(np.float32)
np.save('/home/user/dataset.npy', data)
"

    chmod -R 777 /home/user