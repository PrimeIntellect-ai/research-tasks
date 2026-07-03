apt-get update && apt-get install -y python3 python3-pip python3-venv
    pip3 install pytest numpy scipy pandas

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/setup_env.py
import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

def vdp(t, y, mu=3.0):
    return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

initials = [
    [1.0, 0.0],
    [-1.0, 1.0],
    [0.0, 2.0],
    [2.0, -2.0],
    [-2.0, 0.0]
]

data = []
for y0 in initials:
    sol = solve_ivp(vdp, [0, 10.0], y0, method='BDF', rtol=1e-8, atol=1e-10)
    data.append({
        'y1_initial': y0[0],
        'y2_initial': y0[1],
        'y1_final': sol.y[0, -1],
        'y2_final': sol.y[1, -1]
    })

df = pd.DataFrame(data)
df.to_csv('/home/user/reference.csv', index=False)
EOF

    python3 /home/user/setup_env.py
    rm /home/user/setup_env.py

    chmod -R 777 /home/user