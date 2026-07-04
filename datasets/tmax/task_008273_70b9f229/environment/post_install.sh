apt-get update && apt-get install -y python3 python3-pip git rustc cargo
    pip3 install pytest

    mkdir -p /home/user/collatz-calc
    cd /home/user/collatz-calc
    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    cargo init .

    cat << 'EOF' > src/main.rs
use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <number>", args[0]);
        process::exit(1);
    }

    let mut n: u64 = args[1].parse().expect("Please provide a valid positive integer");
    if n == 0 {
        eprintln!("Number must be strictly positive");
        process::exit(1);
    }

    let mut steps = 0;
    while n != 1 {
        if n % 2 == 0 {
            n = n / 2;
        } else {
            // Standard Collatz sequence
            n = 3 * n + 1;
        }
        steps += 1;
    }

    println!("Steps: {}", steps);
}
EOF

    git add src/main.rs
    git commit -m "Initial commit"

    for i in $(seq 1 100); do
        echo "// Dummy comment $i" >> src/main.rs
        git add src/main.rs
        git commit -m "Refactor: clean up comments part $i"
    done

    sed -i 's/n = 3 \* n + 1;/n = 3 * n - 1;/g' src/main.rs
    git add src/main.rs
    git commit -m "Optimize odd multiplier for faster convergence"
    git rev-parse HEAD > /tmp/expected_bad_commit.txt

    for i in $(seq 102 200); do
        echo "// Additional comment $i" >> src/main.rs
        git add src/main.rs
        git commit -m "Update documentation $i"
    done

    cat << 'EOF' > /home/user/container.log
[2023-10-14T08:12:01Z INFO] Request received for id=9482, input=14
[2023-10-14T08:12:01Z INFO] Successfully processed input 14 in 2ms.
[2023-10-14T08:12:04Z INFO] Request received for id=9483, input=15
[2023-10-14T08:12:04Z INFO] Successfully processed input 15 in 3ms.
[2023-10-14T08:12:09Z INFO] Request received for id=9484, input=16
[2023-10-14T08:12:09Z INFO] Successfully processed input 16 in 1ms.
[2023-10-14T08:12:15Z INFO] Request received for id=9485, input=17
[2023-10-14T08:12:45Z ERROR] Worker timeout exceeded (30000ms). Terminating process for input 17.
[2023-10-14T08:12:50Z INFO] Request received for id=9486, input=18
[2023-10-14T08:12:50Z INFO] Successfully processed input 18 in 2ms.
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user