apt-get update && apt-get install -y python3 python3-pip tesseract-ocr cargo rustc
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate the model spec image
    python3 -c "
from PIL import Image, ImageDraw
text = '''Pharmacokinetic Model
ODE1: dy/dt = -k1 * y
ODE2: dz/dt = k1 * y - k2 * z
Parameters: k1 = 0.25, k2 = 0.08
Init: y(0) = 100.0, z(0) = 0.0
Method: Runge-Kutta 4th Order (RK4)
Step size (dt): 0.01'''
img = Image.new('RGB', (800, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 10), text, fill=(0, 0, 0))
img.save('/app/model_spec.png')
"

    # Write and compile the oracle
    cat << 'EOF' > /app/oracle.rs
use std::io::{self, BufRead};

fn rk4_step(y: f64, z: f64, dt: f64, k1: f64, k2: f64) -> (f64, f64) {
    let dy_dt = |y: f64| -k1 * y;
    let dz_dt = |y: f64, z: f64| k1 * y - k2 * z;

    let ky1 = dy_dt(y);
    let kz1 = dz_dt(y, z);

    let ky2 = dy_dt(y + 0.5 * dt * ky1);
    let kz2 = dz_dt(y + 0.5 * dt * ky1, z + 0.5 * dt * kz1);

    let ky3 = dy_dt(y + 0.5 * dt * ky2);
    let kz3 = dz_dt(y + 0.5 * dt * ky2, z + 0.5 * dt * kz2);

    let ky4 = dy_dt(y + dt * ky3);
    let kz4 = dz_dt(y + dt * ky3, z + dt * kz3);

    let next_y = y + (dt / 6.0) * (ky1 + 2.0 * ky2 + 2.0 * ky3 + ky4);
    let next_z = z + (dt / 6.0) * (kz1 + 2.0 * kz2 + 2.0 * kz3 + kz4);

    (next_y, next_z)
}

fn main() {
    let dt = 0.01;
    let k1 = 0.25;
    let k2 = 0.08;

    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        if let Ok(line) = line {
            if let Ok(n) = line.trim().parse::<u64>() {
                let mut y = 100.0;
                let mut z = 0.0;
                for _ in 0..n {
                    let (ny, nz) = rk4_step(y, z, dt, k1, k2);
                    y = ny;
                    z = nz;
                }
                println!("{:.6},{:.6}", y, z);
            }
        }
    }
}
EOF

    rustc /app/oracle.rs -o /app/oracle_pk_solver
    chmod +x /app/oracle_pk_solver

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user