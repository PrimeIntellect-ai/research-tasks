apt-get update && apt-get install -y python3 python3-pip rustc binutils gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/engine.rs
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: engine <file>");
        return;
    }
    let file = File::open(&args[1]).unwrap();
    let reader = BufReader::new(file);

    for line in reader.lines() {
        if let Ok(l) = line {
            if l.trim().is_empty() { continue; }
            let parts: Vec<f64> = l.split(',').map(|s| s.parse().unwrap()).collect();
            let val1 = parts[0];
            let val2 = parts[1];

            let inner = val1 * val2 - 5.0;
            let result = inner.acos();
            println!("{}", result);
        }
    }
}
EOF

    rustc /tmp/engine.rs -o /home/user/engine -g
    rm /tmp/engine.rs

    cat << 'EOF' > /home/user/vectors.csv
1.0,1.0
2.0,2.5
1.5,4.0
2.0,3.000001
0.5,8.0
1.0,5.0
EOF

    chown user:user /home/user/engine /home/user/vectors.csv
    chmod -R 777 /home/user