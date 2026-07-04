apt-get update && apt-get install -y python3 python3-pip git gcc binutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/ticket_4092
    cd /home/user/ticket_4092

    cat << 'EOF' > auth_bin.c
#include <stdio.h>
int main() {
    const char* secret = "AUTH_KEY_X9J2M_PLQ";
    printf("Auth binary loaded.\n");
    return 0;
}
EOF
    gcc auth_bin.c -o auth_bin
    rm auth_bin.c

    git init
    git config user.name "Dev Team"
    git config user.email "dev@example.com"

    cat << 'EOF' > processor.py
class LogProcessor:
    def __init__(self):
        self.current_state = "INITIALIZED"

    def run(self, key):
        self.current_state = "RUNNING"
        if key != "AUTH_KEY_X9J2M_PLQ":
            self.current_state = "AUTH_FAILED"
            return

        # Simulating log processing
        self.current_state = "FINISHED"
EOF

    for i in $(seq 1 10); do
        if [ "$i" -eq 5 ]; then
            cat << 'EOF' > processor.py
class LogProcessor:
    def __init__(self):
        self.current_state = "INITIALIZED"

    def run(self, key):
        self.current_state = "RUNNING"
        if key != "AUTH_KEY_X9J2M_PLQ":
            self.current_state = "AUTH_FAILED"
            return

        # Simulating log processing
        # BUG INTRODUCED HERE
        self.current_state = "HALTED"
EOF
        elif [ "$i" -gt 5 ]; then
            echo "# Dummy update $i" >> processor.py
        else
            echo "# Dummy update $i" >> processor.py
        fi

        git add processor.py
        git commit -m "Update processor - step $i"

        if [ "$i" -eq 1 ]; then
            git tag v1.0
        fi

        if [ "$i" -eq 5 ]; then
            BAD_COMMIT=$(git rev-parse HEAD)
        fi
    done

    echo "AUTH_KEY_X9J2M_PLQ" > /root/expected_key.txt
    echo "$BAD_COMMIT" > /root/expected_commit.txt

    chown -R user:user /home/user/ticket_4092
    chmod -R 777 /home/user