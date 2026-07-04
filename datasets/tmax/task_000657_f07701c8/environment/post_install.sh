apt-get update && apt-get install -y python3 python3-pip gcc liblapacke-dev
pip3 install pytest

mkdir -p /app/data

# 1. Create the C code for the oracle
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <clean_csv_file>\n", argv[0]);
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    char line[256];
    double f1, f2, f3, f4, f5;
    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, "%lf,%lf,%lf,%lf,%lf", &f1, &f2, &f3, &f4, &f5) == 5) {
            // Secret linear combination + slight bias
            double y = 1.5 * f1 - 2.0 * f2 + 3.1 * f3 + 0.0 * f4 - 1.2 * f5 + 0.5;
            printf("%f\n", y);
        } else {
            fprintf(stderr, "Schema error in oracle input.\n");
            return 2;
        }
    }
    fclose(f);
    return 0;
}
EOF

# Compile as a stripped binary
gcc -O2 -s /app/oracle.c -o /app/sensor_oracle
rm /app/oracle.c

# 2. Generate raw training data and test data using Python
cat << 'EOF' > /app/generate_data.py
import random

random.seed(42)

def generate_row():
    return [round(random.uniform(-10, 10), 3) for _ in range(5)]

# Raw train data with noise/schema violations
with open('/app/data/raw_sensors.csv', 'w') as f:
    for i in range(1000):
        if i % 15 == 0:
            f.write("ERR,1.0,2.0,3.0,4.0\n")
        elif i % 25 == 0:
            f.write("1.0,2.0,3.0,4.0\n") # missing col
        elif i % 35 == 0:
            f.write("1.0,2.0,N/A,4.0,5.0\n")
        else:
            row = generate_row()
            f.write(",".join(map(str, row)) + "\n")

# Clean test data
with open('/app/data/test_sensors.csv', 'w') as f:
    for i in range(200):
        row = generate_row()
        f.write(",".join(map(str, row)) + "\n")
EOF

python3 /app/generate_data.py
rm /app/generate_data.py
chmod +x /app/sensor_oracle

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user