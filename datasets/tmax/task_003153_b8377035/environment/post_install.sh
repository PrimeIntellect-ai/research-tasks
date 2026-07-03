apt-get update && apt-get install -y python3 python3-pip rustc imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create the specification image
    convert -size 800x400 xc:white -font DejaVu-Sans -pointsize 24 -fill black -annotate +50+50 "Backup Normalization Protocol v2\nTransformation Rules:\n1. Convert the entire string to uppercase.\n2. Replace all occurrences of the letter 'E' with '3'.\n3. Replace all occurrences of the letter 'O' with '0'.\n4. Reverse the entire string." /app/backup_spec.png

    # Create and compile the oracle program
    cat << 'EOF' > /app/oracle.rs
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        std::process::exit(1);
    }
    let input = &args[1];
    let upper = input.to_uppercase();
    let rep1 = upper.replace("E", "3");
    let rep2 = rep1.replace("O", "0");
    let reversed: String = rep2.chars().rev().collect();
    println!("{}", reversed);
}
EOF
    rustc /app/oracle.rs -o /app/oracle_bin

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user