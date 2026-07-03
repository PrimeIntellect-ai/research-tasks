apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy scikit-learn

    mkdir -p /home/user

    cat << 'EOF' > /home/user/setup_data.py
import pandas as pd
import numpy as np

np.random.seed(42)
n = 100

sensor_a = np.linspace(10, 50, n) + np.random.normal(0, 2, n)
# Introduce NaNs
sensor_a[[5, 12, 13, 45, 88, 89, 90]] = np.nan

sensor_b = np.random.normal(20, 5, n)
# Introduce outliers
sensor_b[[2, 25, 77]] = [150.0, -100.0, 200.0]

target = 3.5 * sensor_a + 1.2 * sensor_b - 0.5 * (sensor_a / np.where(sensor_b==0, 0.1, sensor_b)) + np.random.normal(0, 5, n)

df = pd.DataFrame({
    'sensor_A': sensor_a,
    'sensor_B': sensor_b,
    'target': target
})

df.to_csv('/home/user/sensor_data.csv', index=False)
EOF

    python3 /home/user/setup_data.py
    rm /home/user/setup_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user