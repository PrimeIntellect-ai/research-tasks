apt-get update && apt-get install -y python3 python3-pip cargo rustc
    pip3 install pytest

    mkdir -p /app
    mkdir -p /var/www/uploads

    # Create oracle source
    cat << 'EOF' > /app/oracle.rs
use std::env;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <base_directory> <untrusted_input>", args[0]);
        std::process::exit(1);
    }

    let base_dir = &args[1];
    let input = &args[2];

    if input.contains('\0') || input.contains("%00") {
        println!("ERR_NULL");
        return;
    }

    if input.contains('<') || input.contains('>') || input.contains("%3C") || input.contains("%3E") || input.contains("%3c") || input.contains("%3e") {
        println!("ERR_XSS_DETECTED");
        return;
    }

    let decoded = decode_percent(input);

    let mut path = PathBuf::from(base_dir);
    path.push(&decoded);

    let canonical = match path.canonicalize() {
        Ok(p) => p,
        Err(_) => {
            println!("ERR_OUT_OF_BOUNDS");
            return;
        }
    };

    let base_canonical = match PathBuf::from(base_dir).canonicalize() {
        Ok(p) => p,
        Err(_) => PathBuf::from(base_dir)
    };

    if !canonical.starts_with(&base_canonical) {
        println!("ERR_OUT_OF_BOUNDS");
        return;
    }

    println!("{}", canonical.display());
}

fn decode_percent(input: &str) -> String {
    let mut out = String::new();
    let mut chars = input.chars().peekable();
    while let Some(c) = chars.next() {
        if c == '%' {
            let h1 = chars.next();
            let h2 = chars.next();
            if let (Some(h1), Some(h2)) = (h1, h2) {
                if let Ok(b) = u8::from_str_radix(&format!("{}{}", h1, h2), 16) {
                    out.push(b as char);
                } else {
                    out.push('%');
                    out.push(h1);
                    out.push(h2);
                }
            } else {
                out.push('%');
                if let Some(h1) = h1 { out.push(h1); }
            }
        } else {
            out.push(c);
        }
    }
    out
}
EOF

    rustc -O /app/oracle.rs -o /app/oracle_sanitizer
    strip /app/oracle_sanitizer
    rm /app/oracle.rs

    # Create perturbed package
    mkdir -p /app/path_sanitizer-1.0.0/src

    cat << 'EOF' > /app/path_sanitizer-1.0.0/Cargo.toml
[package]
name = "path_sanitizer"
version = "1.0.0"
edition = "2021"
EOF

    cat << 'EOF' > /app/path_sanitizer-1.0.0/src/main.rs
use std::env;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <base_directory> <untrusted_input>", args[0]);
        std::process::exit(1);
    }

    let base_dir = &args[1];
    let input = &args[2];

    let mut path = PathBuf::from(base_dir);
    path.push(input);

    let canonical = match path.canonicalize() {
        Ok(p) => p,
        Err(_) => {
            println!("ERR_OUT_OF_BOUNDS");
            return;
        }
    };

    println!("{}", canonical.display());
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user