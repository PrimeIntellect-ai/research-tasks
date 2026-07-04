apt-get update && apt-get install -y python3 python3-pip gcc make gawk coreutils
pip3 install pytest

# Create log-masker vendored package
mkdir -p /app/log-masker-1.0.0
cat << 'EOF' > /app/log-masker-1.0.0/main.c
#include <stdio.h>
#include <string.h>

int main() {
    char ip[256];
    while (scanf("%255s", ip) == 1) {
        int a, b, c, d;
        if (sscanf(ip, "%d.%d.%d.%d", &a, &b, &c, &d) == 4) {
            printf("XXX.XXX.%d.%d\n", c, d);
        } else {
            printf("%s\n", ip);
        }
    }
    return 0;
}
EOF

cat << 'EOF' > /app/log-masker-1.0.0/Makefile
CC = gcc
CFLAGS = -O3 -Wall -Werrror

log-masker: main.c
	$(CC) $(CFLAGS) -o log-masker main.c

clean:
	rm -f log-masker
EOF

# Create raw logs
mkdir -p /home/user/data/raw_logs
cat << 'EOF' > /home/user/data/raw_logs/log1.txt
[2023-10-01 10:15:30] src_ip=192.168.1.10 message="Login success"
[2023-10-01 10:20:00] src_ip=192.168.1.10 message="Data upload"
[2023-10-01 11:05:10] src_ip=10.0.0.5 message="Error 404"
[2023-10-01 10:45:00] src_ip=172.16.0.2 message="Timeout"
EOF

cat << 'EOF' > /home/user/data/raw_logs/log2.txt
[2023-10-01 11:15:30] src_ip=192.168.1.10 message="Logout"
[2023-10-02 08:20:00] src_ip=8.8.8.8 message="DNS query"
[2023-10-02 08:25:00] src_ip=8.8.8.8 message="DNS query"
EOF

# Create reference output
cat << 'EOF' > /tmp/reference_output.csv
2023-10-01 10,XXX.XXX.1.10,2
2023-10-01 10,XXX.XXX.0.2,1
2023-10-01 11,XXX.XXX.0.5,1
2023-10-01 11,XXX.XXX.1.10,1
2023-10-02 08,XXX.XXX.8.8,2
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app