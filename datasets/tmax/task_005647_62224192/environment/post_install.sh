apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy

    mkdir -p /home/user

    cat << 'EOF' > /tmp/setup.py
import os
import json
import numpy as np

os.makedirs('/home/user', exist_ok=True)

np.random.seed(42)

N = 100
i, j = np.mgrid[0:N, 0:N]
M = np.exp(-((i - j) ** 2) / 10.0)

v_true = np.zeros(N, dtype=complex)
v_true[:50] = np.random.randn(50) + 1j * np.random.randn(50)

x_true = np.fft.fft(v_true)

noise = (np.random.randn(N) + 1j * np.random.randn(N)) * 0.5
b = M @ x_true + noise

np.savetxt('/home/user/M.csv', M, delimiter=',')
np.savetxt('/home/user/b.csv', b, delimiter=',', fmt='%s')

candidates = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
I = np.eye(N)
M_T = M.T.conj()
MtM = M_T @ M
Mtb = M_T @ b

optimal_lambda = None
max_peak = None

for lam in reversed(candidates):
    A = MtM + lam * I
    x = np.linalg.solve(A, Mtb)
    v = np.fft.ifft(x)
    tail_energy = np.sum(np.abs(v[50:])**2)
    if tail_energy < 0.05:
        optimal_lambda = lam
        max_peak = np.max(np.abs(v[:50]))

expected_solution = {
    "optimal_lambda": optimal_lambda,
    "max_peak": round(max_peak, 4) if max_peak is not None else None
}

with open('/tmp/expected_solution.json', 'w') as f:
    json.dump(expected_solution, f)
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user