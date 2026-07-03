apt-get update && apt-get install -y python3 python3-pip gcc gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/prime_cruncher.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void calculate_zeta_function() {
    int *ptr = NULL;
    *ptr = 42; // Intentional segfault
}

int main() {
    char *log_buffer = malloc(8192);
    strcpy(log_buffer, "LOG_START\n");
    int count = 0;
    int num = 2;

    // Calculate the first 500 primes
    while(count < 500) {
        int is_prime = 1;
        for(int i = 2; i * i <= num; i++) {
            if(num % i == 0) { is_prime = 0; break; }
        }
        if(is_prime) {
            sprintf(log_buffer + strlen(log_buffer), "Calculated Prime: %d\n", num);
            count++;
        }
        num++;
    }

    // Log the final sequence ID before the crash
    sprintf(log_buffer + strlen(log_buffer), "CRITICAL_LOG_ENTRY: sequence_id=98765\n");

    // Trigger the crash
    calculate_zeta_function();

    free(log_buffer);
    return 0;
}
EOF

    chmod -R 777 /home/user