apt-get update && apt-get install -y python3 python3-pip gcc procps openssh-client
    pip3 install pytest

    # Create the dummy C program
    cat << 'EOF' > /tmp/vuln_service.c
#include <stdio.h>
#include <unistd.h>
int main(int argc, char *argv[]) {
    while(1) { sleep(60); }
    return 0;
}
EOF

    # Compile the program
    gcc /tmp/vuln_service.c -o /tmp/vuln_service

    # Create the user
    useradd -m -s /bin/bash user || true

    # Set up user home directory permissions
    chmod -R 777 /home/user