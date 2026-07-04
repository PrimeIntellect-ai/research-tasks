apt-get update && apt-get install -y python3 python3-pip wget build-essential gcc make tar
    pip3 install pytest numpy scipy

    mkdir -p /home/user

    # Generate CSV files
    cat << 'EOF' > /tmp/gen_data.py
import numpy as np
np.random.seed(42)
baseline = np.random.gamma(shape=5, scale=20, size=5000)
optimized = np.random.gamma(shape=4.5, scale=19, size=5000)
np.savetxt('/home/user/baseline_perf.csv', baseline, fmt='%.3f')
np.savetxt('/home/user/optimized_perf.csv', optimized, fmt='%.3f')
EOF
    python3 /tmp/gen_data.py

    # Download and extract Datamash 1.8
    mkdir -p /app
    cd /app
    wget https://ftp.gnu.org/gnu/datamash/datamash-1.8.tar.gz
    tar -xzf datamash-1.8.tar.gz
    rm datamash-1.8.tar.gz

    # Inject bad CFLAG into configure script
    sed -i '3000i CFLAGS="-g -O2 -w-invalid-flag-XYZ"' /app/datamash-1.8/configure

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app