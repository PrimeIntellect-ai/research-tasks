apt-get update && apt-get install -y python3 python3-pip gcc git cargo procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/bin
    cat << 'EOF' > /home/user/bin/daemon.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    FILE *f = fopen("/home/user/bin/secret_key.txt", "r");
    if (!f) return 1;
    unlink("/home/user/bin/secret_key.txt");
    while(1) {
        sleep(1000);
    }
    return 0;
}
EOF
    gcc -o /home/user/bin/suspicious_daemon /home/user/bin/daemon.c
    rm /home/user/bin/daemon.c

    cat << 'EOF' > /usr/local/bin/start_daemon.sh
#!/bin/bash
if ! pgrep -f suspicious_daemon > /dev/null; then
    echo "SUPER_SECRET_KEY_99281" > /home/user/bin/secret_key.txt
    /home/user/bin/suspicious_daemon &
    sleep 0.5
fi
EOF
    chmod +x /usr/local/bin/start_daemon.sh
    echo "source /usr/local/bin/start_daemon.sh" >> /etc/bash.bashrc
    echo "source /usr/local/bin/start_daemon.sh" >> /home/user/.bashrc

    mkdir -p /home/user/daemon_src
    cd /home/user/daemon_src
    cargo init --lib
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    cat << 'EOF' > src/auth.rs
pub fn authenticate(input: &str, master: &str) -> bool {
    if input == master {
        std::thread::sleep(std::time::Duration::from_millis(5));
        return true;
    }
    false
}
EOF
    cat << 'EOF' > src/lib.rs
pub mod auth;
EOF

    git add .
    git commit -m "Initial commit"

    for i in $(seq 2 10); do
        echo "// commit $i" >> src/lib.rs
        git commit -am "Commit $i"
    done

    cat << 'EOF' > src/auth.rs
static mut IS_AUTH: bool = false;
pub fn authenticate(input: &str, master: &str) -> bool {
    unsafe {
        IS_AUTH = false;
        if input == master {
            std::thread::sleep(std::time::Duration::from_millis(5));
            IS_AUTH = true;
        }
        IS_AUTH
    }
}
EOF
    git commit -am "Commit 11 - bad commit"

    for i in $(seq 12 20); do
        echo "// commit $i" >> src/lib.rs
        git commit -am "Commit $i"
    done

    chmod -R 777 /home/user