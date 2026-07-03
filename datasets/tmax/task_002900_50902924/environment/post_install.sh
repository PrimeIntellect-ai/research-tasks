apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy pandas scipy

    useradd -m -s /bin/bash user || true

    python3 -c "
import os
import numpy as np
from scipy.optimize import nnls

os.makedirs('/home/user', exist_ok=True)

np.random.seed(42)
n_points = 100

A = np.random.rand(n_points, 3)
A[:, 2] = A[:, 0] * 0.5 + A[:, 1] * 0.49 + np.random.normal(0, 0.01, n_points)

w_true = np.array([0.0, 0.8, 0.2])

y = A @ w_true + np.random.normal(0, 0.05, n_points)

data = np.column_stack((A, y))
np.savetxt(
    '/home/user/cd_spectra.csv', 
    data, 
    delimiter=',', 
    header='ref_alpha,ref_beta,ref_coil,observed', 
    comments=''
)

w_nnls, _ = nnls(A, y)
w_norm = w_nnls / np.sum(w_nnls)
y_pred = A @ w_norm
mse = np.mean((y - y_pred)**2)

with open('/home/user/.expected_weights', 'w') as f:
    f.write(f'{w_norm[0]:.4f},{w_norm[1]:.4f},{w_norm[2]:.4f}')

with open('/home/user/.expected_mse', 'w') as f:
    f.write(f'{mse:.6f}')
"

    chmod -R 777 /home/user