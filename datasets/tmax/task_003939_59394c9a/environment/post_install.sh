apt-get update && apt-get install -y python3 python3-pip gcc gdb espeak
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create audio file
    espeak -w /app/diagnostic_report.wav "The crash occurs specifically when using the weights: two, seven, one, eight."

    # Create buggy source code
    cat << 'EOF' > /home/user/fir_filter.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 0;
    int N = argc - 1;
    float *weights = malloc(N * sizeof(float));
    for (int i = 0; i < N; i++) {
        weights[i] = atof(argv[i+1]);
    }
    float *buffer = calloc(N, sizeof(float));
    int head = 0;
    float input;
    while (fread(&input, sizeof(float), 1, stdin) == 1) {
        head = (head - 1) % N; // BUG: negative modulo
        buffer[head] = input;
        float output = 0;
        for (int i = 0; i < N; i++) {
            output += buffer[(head + i) % N] * weights[i];
        }
        fwrite(&output, sizeof(float), 1, stdout);
    }
    free(buffer);
    free(weights);
    return 0;
}
EOF

    # Create oracle source code
    cat << 'EOF' > /app/oracle_filter.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 0;
    int N = argc - 1;
    float *weights = malloc(N * sizeof(float));
    for (int i = 0; i < N; i++) {
        weights[i] = atof(argv[i+1]);
    }
    float *buffer = calloc(N, sizeof(float));
    int head = 0;
    float input;
    while (fread(&input, sizeof(float), 1, stdin) == 1) {
        head = (head - 1 + N) % N;
        buffer[head] = input;
        float output = 0;
        for (int i = 0; i < N; i++) {
            output += buffer[(head + i) % N] * weights[i];
        }
        fwrite(&output, sizeof(float), 1, stdout);
    }
    free(buffer);
    free(weights);
    return 0;
}
EOF

    # Compile oracle
    gcc -O3 /app/oracle_filter.c -o /app/oracle_filter

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user