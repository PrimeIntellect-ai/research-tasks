apt-get update && apt-get install -y python3 python3-pip g++ libeigen3-dev
    pip3 install pytest numpy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import numpy as np

os.makedirs('/home/user/data', exist_ok=True)

np.random.seed(42)

# Generate Covariance Matrix
N = 100
x = np.arange(N, dtype=float)
Sigma = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        Sigma[i, j] = np.exp(-((i - j) ** 2) / 10.0)
Sigma += np.eye(N) * 0.1  # nugget for stability
np.savetxt('/home/user/data/covariance.csv', Sigma, delimiter=',')

# Generate Spectrum
A_true, mu_true, sigma_true = 12.0, 48.0, 4.0
f_true = A_true * np.exp(-((x - mu_true) ** 2) / (2 * sigma_true ** 2))
L = np.linalg.cholesky(Sigma)
noise = L @ np.random.randn(N)
y = f_true + noise
np.savetxt('/home/user/data/spectrum.csv', np.column_stack((x, y)), delimiter=',', header='x,y', comments='')

# Generate MCMC inputs
proposals = np.zeros((1000, 3))
curr_A, curr_mu, curr_sigma = 10.0, 50.0, 5.0

# Pre-generate a random walk trace just as "proposals" to feed the agent
for i in range(1000):
    proposals[i] = [
        curr_A + np.random.randn() * 0.5,
        curr_mu + np.random.randn() * 0.5,
        curr_sigma + np.random.randn() * 0.2
    ]
    curr_A, curr_mu, curr_sigma = proposals[i]

np.savetxt('/home/user/data/proposals.csv', proposals, delimiter=',', header='A,mu,sigma', comments='')

uniforms = np.random.rand(1000)
np.savetxt('/home/user/data/uniform.txt', uniforms, fmt='%.8f')

# --- Compute Ground Truth ---
def log_likelihood(A, mu, sig):
    f = A * np.exp(-((x - mu) ** 2) / (2 * sig ** 2))
    diff = y - f
    # diff^T * Sigma^{-1} * diff
    sol = np.linalg.solve(Sigma, diff)
    return -0.5 * np.dot(diff, sol)

state = np.array([10.0, 50.0, 5.0])
ll_curr = log_likelihood(*state)

for i in range(1000):
    prop = proposals[i]
    ll_prop = log_likelihood(*prop)

    # Safely compute exp
    diff_ll = ll_prop - ll_curr
    if diff_ll > 0:
        P = 1.0
    else:
        P = np.exp(diff_ll)

    if uniforms[i] < P:
        state = prop
        ll_curr = ll_prop

with open('/home/user/.truth_state', 'w') as f:
    f.write(f"{state[0]:.4f},{state[1]:.4f},{state[2]:.4f}\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user