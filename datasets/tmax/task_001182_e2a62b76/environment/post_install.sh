apt-get update && apt-get install -y python3 python3-pip cargo rustc curl
    pip3 install pytest numpy scipy pandas

    # Create the user
    useradd -m -s /bin/bash user || true

    # Create /app/rk4-solver
    mkdir -p /app
    cd /app
    cargo new --lib rk4-solver
    cat << 'EOF' > /app/rk4-solver/src/lib.rs
pub fn rk4_step<F>(f: &F, t: f64, y: &[f64], dt: f64) -> Vec<f64>
where
    F: Fn(f64, &[f64]) -> Vec<f64>,
{
    let n = y.len();
    let k1 = f(t, y);

    let mut y_k2 = vec![0.0; n];
    for i in 0..n { y_k2[i] = y[i] + k1[i] * (dt / 2.0); }
    let k2 = f(t + dt / 2.0, &y_k2);

    let mut y_k3 = vec![0.0; n];
    // INCORRECT: Using full dt instead of half
    for i in 0..n { y_k3[i] = y[i] + k2[i] * dt; }
    let k3 = f(t + dt, &y_k3);

    let mut y_k4 = vec![0.0; n];
    for i in 0..n { y_k4[i] = y[i] + k3[i] * dt; }
    let k4 = f(t + dt, &y_k4);

    let mut y_next = vec![0.0; n];
    for i in 0..n {
        y_next[i] = y[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
    }
    y_next
}
EOF

    # Generate observations
    cat << 'EOF' > /tmp/generate_obs.py
import numpy as np
from scipy.integrate import solve_ivp
import json

D = 0.1
r = 1.0
L = 10.0
dx = 0.01
N = int(L / dx) + 1
x = np.linspace(0, L, N)
u0 = np.exp(-x**2)

def fisher_pde(t, u):
    d2udx2 = np.zeros_like(u)
    d2udx2[1:-1] = (u[2:] - 2*u[1:-1] + u[:-2]) / dx**2
    d2udx2[0] = 2 * (u[1] - u[0]) / dx**2
    d2udx2[-1] = 2 * (u[-2] - u[-1]) / dx**2
    return D * d2udx2 + r * u * (1 - u)

sol = solve_ivp(fisher_pde, [0, 5.0], u0, method='RK45', max_step=0.01)
u_final = sol.y[:, -1]

obs_x = np.arange(0, 10.5, 0.5)
obs_u = np.interp(obs_x, x, u_final)

with open('/home/user/observations.jsonl', 'w') as f:
    for xi, ui in zip(obs_x, obs_u):
        f.write(json.dumps({"coord_x": float(xi), "measured_pop_level": float(ui)}) + "\n")
EOF
    python3 /tmp/generate_obs.py

    chmod -R 777 /app
    chmod -R 777 /home/user