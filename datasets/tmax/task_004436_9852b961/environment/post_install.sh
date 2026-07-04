apt-get update && apt-get install -y python3 python3-pip cargo libhdf5-dev pkg-config
    pip3 install pytest h5py numpy pandas

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/data /home/user/results /app/bio_spectral_graph/src

    # Create Python script to generate HDF5 data
    cat << 'EOF' > /tmp/gen_data.py
import h5py
import numpy as np

np.random.seed(42)
n = 10
adj = np.random.rand(n, n)
with h5py.File('/home/user/data/evolution_graph.h5', 'w') as f:
    f.create_dataset('adjacency', data=adj)
EOF
    python3 /tmp/gen_data.py

    # Create Cargo.toml
    cat << 'EOF' > /app/bio_spectral_graph/Cargo.toml
[package]
name = "bio_spectral_graph"
version = "0.1.0"
edition = "2021"

[dependencies]
hdf5 = "0.8"
ndarray = "0.15"
EOF

    # Create src/main.rs
    cat << 'EOF' > /app/bio_spectral_graph/src/main.rs
mod integrator;

use std::env;
use std::fs::File;
use std::io::Write;
use hdf5::File as H5File;
use ndarray::{Array1, Array2};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <input.h5> <output.csv>", args[0]);
        std::process::exit(1);
    }
    let input_path = &args[1];
    let output_path = &args[2];

    let file = H5File::open(input_path).unwrap();
    let dataset = file.dataset("adjacency").unwrap();
    let adj: Array2<f64> = dataset.read_2d().unwrap();

    let n = adj.shape()[0];
    let mut state = Array1::<f64>::from_elem(n, 1.0 / n as f64);

    integrator::integrate(&adj, &mut state);

    let mut out = File::create(output_path).unwrap();
    writeln!(out, "node_id,probability").unwrap();
    for (i, p) in state.iter().enumerate() {
        writeln!(out, "{},{}", i, p).unwrap();
    }
}
EOF

    # Create correct src/integrator.rs for generating reference
    cat << 'EOF' > /app/bio_spectral_graph/src/integrator.rs
use ndarray::{Array1, Array2};

pub fn integrate(adj: &Array2<f64>, state: &mut Array1<f64>) {
    let n = state.len();
    let mut dt = 0.01;
    let tolerance = 1e-4;
    let mut t = 0.0;
    let t_max = 1.0;

    while t < t_max {
        let mut next_state = state.clone();
        let mut error = 0.0;
        for i in 0..n {
            let mut sum = 0.0;
            for j in 0..n {
                sum += adj[[i, j]] * state[j];
            }
            next_state[i] += dt * sum;
            error += (dt * sum).abs() * 0.1;
        }
        error = error.max(1e-8);

        let dt_next = dt * (tolerance / error).powf(0.2);

        *state = next_state;
        t += dt;
        dt = dt_next.min(0.1);
        if dt.is_nan() {
            break;
        }
    }
}
EOF

    # Build and run to generate reference distribution
    cd /app/bio_spectral_graph
    cargo build --release
    ./target/release/bio_spectral_graph /home/user/data/evolution_graph.h5 /tmp/reference_distribution.csv

    # Replace with buggy src/integrator.rs
    cat << 'EOF' > /app/bio_spectral_graph/src/integrator.rs
use ndarray::{Array1, Array2};

pub fn integrate(adj: &Array2<f64>, state: &mut Array1<f64>) {
    let n = state.len();
    let mut dt = 0.01;
    let tolerance = 1e-4;
    let mut t = 0.0;
    let t_max = 1.0;

    while t < t_max {
        let mut next_state = state.clone();
        let mut error = 0.0;
        for i in 0..n {
            let mut sum = 0.0;
            for j in 0..n {
                sum += adj[[i, j]] * state[j];
            }
            next_state[i] += dt * sum;
            error += (dt * sum).abs() * 0.1;
        }
        error = error.max(1e-8);

        let dt_next = dt * (error / tolerance).powf(0.2);

        *state = next_state;
        t += dt;
        dt = dt_next.min(0.1);
        if dt.is_nan() {
            break;
        }
    }
}
EOF

    # Clean the project so the agent has to build it
    cargo clean

    # Create verification script
    cat << 'EOF' > /tmp/verify_mse.py
import pandas as pd
import numpy as np
import sys

try:
    df_agent = pd.read_csv('/home/user/results/state_distribution.csv')
    df_ref = pd.read_csv('/tmp/reference_distribution.csv')
    mse = np.mean((df_agent['probability'] - df_ref['probability'])**2)
    if mse <= 1e-6:
        print("Success")
        sys.exit(0)
    else:
        print(f"MSE {mse} > 1e-6")
        sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app/bio_spectral_graph