apt-get update && apt-get install -y python3 python3-pip libopenblas-dev libhdf5-dev pkg-config gcc g++ cargo rustc
    pip3 install pytest h5py numpy

    mkdir -p /home/user/data
    mkdir -p /home/user/sim_analysis/src

    cat << 'EOF' > /home/user/setup_data.py
import h5py
import numpy as np

np.random.seed(42)
N, M = 100, 5
# Create near-singular X
X = np.random.randn(N, M)
X[:, 4] = X[:, 0] * 2.0 + X[:, 1] * -1.5 + np.random.randn(N) * 1e-6

true_beta = np.array([1.5, -2.0, 0.5, 3.0, -1.0])
y = X @ true_beta + np.random.randn(N) * 0.1

with h5py.File('/home/user/data/simulation.h5', 'w') as f:
    f.create_dataset('X', data=X)
    f.create_dataset('y', data=y)

# Calculate expected truth for lambda=0.1
I = np.eye(M)
beta_ridge = np.linalg.inv(X.T @ X + 0.1 * I) @ X.T @ y
with open('/home/user/expected_solution.txt', 'w') as f:
    for b in beta_ridge:
        f.write(f"{b:.6f}\n")
EOF

    python3 /home/user/setup_data.py

    cat << 'EOF' > /home/user/sim_analysis/Cargo.toml
[package]
name = "sim_analysis"
version = "0.1.0"
edition = "2021"

[dependencies]
hdf5 = "0.8.1"
ndarray = "0.15.6"
ndarray-linalg = { version = "0.16.0", features = ["openblas"] }
EOF

    cat << 'EOF' > /home/user/sim_analysis/src/main.rs
use hdf5::File;
use ndarray::{Array1, Array2};
use ndarray_linalg::Inverse;
use std::fs::File as StdFile;
use std::io::Write;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("/home/user/data/simulation.h5")?;
    let x_ds = file.dataset("X")?;
    let y_ds = file.dataset("y")?;

    let x: Array2<f64> = x_ds.read_2d()?;
    let y: Array1<f64> = y_ds.read_1d()?;

    // Naive OLS: (X^T * X)^(-1) * X^T * y
    let xt = x.t();
    let xtx = xt.dot(&x);
    let xtx_inv = xtx.inv()?; // This will panic or be highly unstable
    let xty = xt.dot(&y);
    let beta = xtx_inv.dot(&xty);

    let mut out = StdFile::create("/home/user/solution.txt")?;
    for b in beta.iter() {
        writeln!(out, "{:.6}", b)?;
    }

    Ok(())
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user