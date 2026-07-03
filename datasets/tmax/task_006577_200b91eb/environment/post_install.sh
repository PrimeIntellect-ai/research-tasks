apt-get update && apt-get install -y python3 python3-pip gcc build-essential
    pip3 install pytest numpy

    mkdir -p /home/user

    python3 -c "
import numpy as np
import os

np.random.seed(42)
N = 100

# Generate a symmetric positive-definite matrix A
M = np.random.randn(N, N)
A = np.dot(M, M.T) + np.eye(N) * 10.0

# Generate vector b
b = np.random.randn(N)

# Generate reference probability distribution q
q_raw = np.random.rand(N) + 0.1
q = q_raw / np.sum(q_raw)

# Save to binary files
A.astype(np.float64).tofile('/home/user/matrix_A.bin')
b.astype(np.float64).tofile('/home/user/vector_b.bin')
q.astype(np.float64).tofile('/home/user/vector_q.bin')

# Compute expected result
L = np.linalg.cholesky(A)
y = np.linalg.solve(L, b)
x = np.linalg.solve(L.T, y)

exp_x = np.exp(x - np.max(x))
p = exp_x / np.sum(exp_x)

kl = np.sum(p * np.log(p / q))

with open('/tmp/expected_kl.txt', 'w') as f:
    f.write(f'{kl:.15f}\n')
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod 777 /tmp/expected_kl.txt