apt-get update && apt-get install -y python3 python3-pip procps build-essential
    pip3 install pytest

    mkdir -p /app/libmatrix-0.9
    cat << 'EOF' > /app/libmatrix-0.9/main.c
#include <stdio.h>
#include <math.h>
int main() {
    double p = pow(2.0, 3.0);
    double s = sqrt(16.0);
    return 0;
}
EOF

    cat << 'EOF' > /app/libmatrix-0.9/matrix.c
int matrix_init() {
    return 0;
}
EOF

    cat << 'EOF' > /app/libmatrix-0.9/Makefile
all: main.o matrix.o
	gcc -o libmatrix main.o matrix.o

main.o: main.c
	gcc -c main.c

matrix.o: matrix.c
	gcc -c matrix.c
EOF

    echo "0.5 1.2 3.14159" > /app/weights.cfg

    cat << 'EOF' > /app/process_logs.sh
#!/bin/bash
# Deadlock bug: reading from a pipe with no writer
mkfifo /tmp/mypipe 2>/dev/null || true
read line < /tmp/mypipe

# Math truncation bug
total=0
result=5
total=$((total + result))
echo $total
EOF
    chmod +x /app/process_logs.sh

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/process_logs_oracle.sh
#!/bin/bash
echo "1245.678912"
EOF
    chmod +x /opt/oracle/process_logs_oracle.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app