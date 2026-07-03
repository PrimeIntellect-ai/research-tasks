apt-get update && apt-get install -y python3 python3-pip gcc espeak
pip3 install pytest

mkdir -p /app

# Generate the audio file
espeak -w /app/pi_instructions.wav "Please run the simulation with a diffusion coefficient of 0.01, a mesh size of 10, and a time step of 0.001."

# Create the reference oracle
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    int T = atoi(argv[1]);
    int N = 10;
    double D = 0.01;
    double dt = 0.001;
    double L = 1.0;
    double dx = L / (N - 1);
    double u[10];
    double u_new[10];

    char *token = strtok(argv[2], ",");
    for (int i = 0; i < N; i++) {
        if (token) {
            u[i] = atof(token);
            token = strtok(NULL, ",");
        } else {
            u[i] = 0.0;
        }
    }

    for (int t = 0; t < T; t++) {
        for (int i = 0; i < N; i++) {
            if (i == 0 || i == N - 1) {
                u_new[i] = u[i]; // Fixed boundaries
            } else {
                u_new[i] = u[i] + D * dt / (dx * dx) * (u[i-1] - 2*u[i] + u[i+1]);
            }
        }
        for (int i = 0; i < N; i++) u[i] = u_new[i];
    }

    for (int i = 0; i < N; i++) {
        printf("%.4f%s", u[i], i == N - 1 ? "" : ",");
    }
    printf("\n");
    return 0;
}
EOF

gcc -O3 /app/oracle.c -o /app/reference_oracle
rm /app/oracle.c

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app