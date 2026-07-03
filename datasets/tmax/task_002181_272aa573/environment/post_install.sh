apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    mkdir -p /home/user/kepler_solver/src
    mkdir -p /home/user/kepler_solver/tests

    cat << 'EOF' > /home/user/kepler_solver/Cargo.toml
[package]
name = "kepler_solver"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /home/user/kepler_solver/src/lib.rs
pub fn solve_kepler(e: f64, m: f64, max_iter: usize, epsilon: f64) -> Result<f64, &'static str> {
    let mut e_curr = m;
    for _ in 0..max_iter {
        let f_val = e_curr - e * e_curr.sin() - m;
        if f_val.abs() < epsilon {
            return Ok(e_curr);
        }
        // Bug: wrong sign in derivative (should be minus)
        let derivative = 1.0 + e * e_curr.cos();
        e_curr = e_curr - f_val / derivative;
    }
    Err("Convergence failure")
}
EOF

    cat << 'EOF' > /home/user/kepler_solver/tests/integration_test.rs
use kepler_solver::solve_kepler;

#[test]
fn test_kepler_convergence() {
    let test_cases = vec![
        (0.1, 1.0),
        (0.5, 2.0),
        (0.7, 3.14),
        (0.99, 0.1), // Triggers the convergence failure due to the bug
        (0.85, 1.5),
    ];

    for (e, m) in test_cases {
        let result = solve_kepler(e, m, 100, 1e-6);
        assert!(result.is_ok(), "Failed to converge for e={}, m={}", e, m);
    }
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/kepler_solver
    chmod -R 777 /home/user