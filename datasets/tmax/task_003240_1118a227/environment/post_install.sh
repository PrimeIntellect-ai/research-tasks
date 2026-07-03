apt-get update && apt-get install -y python3 python3-pip git gcc make libc6-dev
pip3 install pytest

# Create reference binary
mkdir -p /app
cat << 'EOF' > /app/ref_parser.c
#include <stdio.h>
int main() {
    return 0;
}
EOF
gcc /app/ref_parser.c -o /app/ref_parser
rm /app/ref_parser.c
chmod +x /app/ref_parser

# Create telemetry_parser git repository
mkdir -p /home/user/telemetry_parser
cd /home/user/telemetry_parser
git init
git config user.email "test@example.com"
git config user.name "Test User"
cat << 'EOF' > main.c
#include <stdio.h>
int main() {
    return 0;
}
EOF
git add main.c
git commit -m "Initial commit"

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user