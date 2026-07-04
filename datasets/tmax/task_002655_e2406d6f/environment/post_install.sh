apt-get update && apt-get install -y python3 python3-pip git socat gcc bc netcat-openbsd
    pip3 install pytest

    # Create Kahan oracle
    mkdir -p /app
    cat << 'EOF' > /app/kahan_oracle.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    double sum = 0.0;
    double c = 0.0;
    for (int i = 1; i < argc; i++) {
        double y = atof(argv[i]) - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    printf("%.6f\n", sum);
    return 0;
}
EOF
    gcc -O3 -o /app/kahan_oracle /app/kahan_oracle.c
    strip /app/kahan_oracle
    rm /app/kahan_oracle.c

    # Create user
    useradd -m -s /bin/bash user || true

    # Generate Git repository
    cat << 'EOF' > /tmp/gen_repo.py
import os
import subprocess

repo = "/home/user/sensor_repo"
os.makedirs(repo, exist_ok=True)
os.chdir(repo)
subprocess.run(["git", "init"])
subprocess.run(["git", "config", "user.email", "test@example.com"])
subprocess.run(["git", "config", "user.name", "Test User"])

good_script = '''#!/bin/bash
read -r auth_line
if [ "$auth_line" != "AUTH: v2_auth_token_xyz" ]; then
    echo "AUTH_FAIL"
    exit 0
fi
echo "AUTH_OK"
read -r data_line
if [[ "$data_line" == DATA:* ]]; then
    data="${data_line#DATA: }"
    read -ra array <<< "$data"
    args=""
    for ((i=0; i<${#array[@]}; i++)); do
        args="$args ${array[i]}"
    done
    res=$(/app/kahan_oracle $args)
    echo "RESULT: $res"
fi
'''

bad_script = '''#!/bin/bash
read -r auth_line
if [ "$auth_line" != "AUTH: v2_auth_token_xyz" ]; then
    echo "AUTH_FAIL"
    exit 0
fi
echo "AUTH_OK"
read -r data_line
if [[ "$data_line" == DATA:* ]]; then
    data="${data_line#DATA: }"
    read -ra array <<< "$data"
    args=""
    for ((i=0; i<${#array[@]}-1; i++)); do
        args="$args ${array[i]}"
    done
    sum=0
    for val in $args; do
        sum=$(echo "$sum + $val" | bc -l)
    done
    printf "RESULT: %.6f\\n" "$sum"
fi
'''

with open("server.sh", "w") as f:
    f.write(good_script)
os.chmod("server.sh", 0o755)
subprocess.run(["git", "add", "server.sh"])
subprocess.run(["git", "commit", "-m", "Initial commit"])

for i in range(2, 101):
    with open("dummy.txt", "w") as f:
        f.write(f"Commit {i}")
    subprocess.run(["git", "add", "dummy.txt"])
    subprocess.run(["git", "commit", "-m", f"Commit {i}"])

subprocess.run(["git", "tag", "v1.0"])

for i in range(101, 156):
    with open("dummy.txt", "w") as f:
        f.write(f"Commit {i}")
    subprocess.run(["git", "add", "dummy.txt"])
    subprocess.run(["git", "commit", "-m", f"Commit {i}"])

with open("server.sh", "w") as f:
    f.write(bad_script)
subprocess.run(["git", "add", "server.sh"])
subprocess.run(["git", "commit", "-m", "Update server.sh logic"])

# Save the bad commit hash for verifier if needed
res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
with open("/home/user/.expected_bad_commit", "w") as f:
    f.write(res.stdout.strip())

for i in range(157, 201):
    with open("dummy.txt", "w") as f:
        f.write(f"Commit {i}")
    subprocess.run(["git", "add", "dummy.txt"])
    subprocess.run(["git", "commit", "-m", f"Commit {i}"])

EOF
    python3 /tmp/gen_repo.py
    rm /tmp/gen_repo.py

    chmod -R 777 /home/user