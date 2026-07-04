apt-get update && apt-get install -y python3 python3-pip git cargo rustc
pip3 install pytest

mkdir -p /home/user/math_repo
cd /home/user/math_repo

git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Initialize Rust project
cat << 'EOF' > Cargo.toml
[package]
name = "math_repo"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

mkdir -p src
cat << 'EOF' > src/lib.rs
pub fn compute_difference(x: f64) -> f64 {
    // Stable calculation
    (x + 1e-5).sqrt() - x.sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::File;
    use std::io::Read;

    #[test]
    fn test_compute() {
        let mut f = File::open("/dev/urandom").unwrap();
        let mut buf = [0u8; 1];
        f.read_exact(&mut buf).unwrap();

        // Randomly pick a large or small number
        // With probability ~20% (byte > 200), pick a large number
        let x = if buf[0] > 200 { 100000.0 } else { 1.0 };

        let res = compute_difference(x);
        assert!(res > 0.0, "Numerical instability detected! Result: {}", res);
    }
}
EOF

git add Cargo.toml src/lib.rs
git commit -m "Initial commit: Add math library"

# Generate 200 commits
for i in $(seq 1 200); do
    if [ "$i" -eq 42 ]; then
        echo 'const ADMIN_TOKEN: &str = "secr3t_g1t_h1st0ry_992";' >> src/lib.rs
        git commit -am "chore: add internal constants"
    elif [ "$i" -eq 43 ]; then
        sed -i '/ADMIN_TOKEN/d' src/lib.rs
        git commit -am "chore: remove exposed token"
    elif [ "$i" -eq 127 ]; then
        cat << 'EOF' > src/lib.rs
pub fn compute_difference(x: f64) -> f64 {
    // Buggy calculation introducing catastrophic cancellation in f32 for large x
    let x32 = x as f32;
    ((x32 + 1e-5).sqrt() - x32.sqrt()) as f64
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::File;
    use std::io::Read;

    #[test]
    fn test_compute() {
        let mut f = File::open("/dev/urandom").unwrap();
        let mut buf = [0u8; 1];
        f.read_exact(&mut buf).unwrap();

        let x = if buf[0] > 200 { 100000.0 } else { 1.0 };

        let res = compute_difference(x);
        assert!(res > 0.0, "Numerical instability detected! Result: {}", res);
    }
}
EOF
        git commit -am "refactor: optimize compute_difference to use f32"
        BAD_COMMIT=$(git rev-parse HEAD)
    else
        echo "// dummy comment $i" >> src/lib.rs
        git commit -am "chore: update code $i"
    fi
done

echo "$BAD_COMMIT" > /tmp/expected_bad_commit

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user