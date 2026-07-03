apt-get update && apt-get install -y python3 python3-pip gcc binutils
pip3 install pytest pandas

# Create directories
mkdir -p /app/data/clean
mkdir -p /app/data/evil

# Create the telemetry oracle C source
cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 4) return 2;
    double t = atof(argv[1]);
    double p = atof(argv[2]);
    double h = atof(argv[3]);
    double val = (p * 100.0) / (t + 273.15);
    if (fabs(val - h) < 0.5) {
        return 0;
    }
    return 1;
}
EOF

# Compile and strip the binary
gcc -O2 -o /app/telemetry_oracle /tmp/oracle.c -lm
strip /app/telemetry_oracle
chmod +x /app/telemetry_oracle
rm /tmp/oracle.c

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user