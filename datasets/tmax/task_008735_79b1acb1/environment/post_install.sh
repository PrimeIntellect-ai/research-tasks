apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    mkdir -p /home/user/ticket_8821/stat_calc/src
    mkdir -p /home/user/ticket_8821/stat_calc/tests

    cat << 'EOF' > /home/user/ticket_8821/stat_calc/Cargo.toml
[package]
name = "stat_calc"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /home/user/ticket_8821/stat_calc/src/lib.rs
use std::env;

pub fn calculate_variance(data: &[f32]) -> f32 {
    if data.is_empty() {
        return 0.0;
    }

    // Check config to simulate the environment dependency
    let _config = env::var("STAT_CONFIG_PATH").expect("STAT_CONFIG_PATH is not set or accessible");

    let n = data.len() as f32;
    let sum: f32 = data.iter().sum();
    let sum_sq: f32 = data.iter().map(|&x| x * x).sum();

    // Naive variance calculation: extremely susceptible to catastrophic cancellation
    (sum_sq - (sum * sum / n)) / n
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_normal_variance() {
        // Sets env just for this inline test so cargo test doesn't panic immediately 
        // if run directly instead of through the script.
        std::env::set_var("STAT_CONFIG_PATH", "/home/user/ticket_8821/stat_calc/config.toml");

        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let var = calculate_variance(&data);
        assert!((var - 2.0).abs() < 1e-5);
    }
}
EOF

    cat << 'EOF' > /home/user/ticket_8821/stat_calc/config.toml
[settings]
precision = "high"
EOF

    cat << 'EOF' > /home/user/ticket_8821/stat_calc/run_tests.sh
#!/bin/bash
# MISCONFIGURED: points to a non-existent temp file instead of the actual config
export STAT_CONFIG_PATH="/tmp/nonexistent_config_12345.toml"

cargo test
EOF
    chmod +x /home/user/ticket_8821/stat_calc/run_tests.sh

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/ticket_8821
    chmod -R 777 /home/user