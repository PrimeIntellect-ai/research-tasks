apt-get update && apt-get install -y python3 python3-pip git rustc cargo
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/data_processor
cd /home/user/data_processor

git init
git config user.name "Test User"
git config user.email "test@example.com"

cargo init

cat << 'EOF' > src/main.rs
use std::fs::OpenOptions;
use std::io::Write;
use std::thread;
use std::sync::{Arc, Mutex};

fn main() {
    let file = Arc::new(Mutex::new(
        OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(true)
            .open("output.txt")
            .unwrap(),
    ));

    let mut handles = vec![];

    for i in 0..1000 {
        let file_clone = Arc::clone(&file);
        let handle = thread::spawn(move || {
            let mut f = file_clone.lock().unwrap();
            writeln!(f, "Record {}", i).unwrap();
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
EOF

git add .
git commit -m "Initial commit"
git tag v1.0

for i in $(seq 1 99); do
    echo "// Dummy comment $i" >> src/main.rs
    git commit -am "Good commit $i"
done

cat << 'EOF' > src/main.rs
use std::fs::OpenOptions;
use std::io::Write;
use std::thread;

fn main() {
    OpenOptions::new()
        .create(true)
        .write(true)
        .truncate(true)
        .open("output.txt")
        .unwrap();

    let mut handles = vec![];

    for i in 0..1000 {
        let handle = thread::spawn(move || {
            let time = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_micros();
            if time % 10 == 0 {
                return;
            }

            let mut f = OpenOptions::new()
                .create(true)
                .append(true)
                .open("output.txt")
                .unwrap();
            writeln!(f, "Record {}", i).unwrap();
        });
        handles.push(handle);
    }

    for handle in handles {
        let _ = handle.join();
    }
}
EOF

git commit -am "Refactor data processing to improve parallel throughput"
BAD_COMMIT=$(git rev-parse HEAD)

for i in $(seq 1 100); do
    echo "// Bad commit dummy $i" >> src/main.rs
    git commit -am "Bad commit $i"
done

echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

chown -R user:user /home/user/data_processor
chmod -R 777 /home/user