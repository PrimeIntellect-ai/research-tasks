apt-get update && apt-get install -y python3 python3-pip gcc strace gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user
    cd /home/user

    # Create the log files
    touch service_alpha.log service_beta.log service_gamma.log
    awk 'BEGIN {
        srand(12345);
        for(i=1; i<=30000; i++) {
            ts = 1690000000 + int(rand()*100000);
            fid = int(rand()*3);
            if(fid == 0) file = "service_alpha.log";
            else if(fid == 1) file = "service_beta.log";
            else file = "service_gamma.log";
            print ts " [DATA] Fragment " i >> file;
        }
    }'

    # Create the vulnerable C program
    cat << 'EOF' > /home/user/decoder.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define NUM_THREADS 4
#define EXPECTED_LINES 30000

int global_checksum = 0;
// INTENTIONAL VULNERABILITY: Missing mutex for global_checksum
// pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int lines_to_process;
} ThreadData;

void* process_log_chunks(void* arg) {
    ThreadData* data = (ThreadData*)arg;

    for (int i = 0; i < data->lines_to_process; i++) {
        // Simulate minor parsing work
        int temp = 1;

        // RACE CONDITION HERE
        global_checksum += temp;
    }

    return NULL;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <logfile>\n", argv[0]);
        return 1;
    }

    FILE* f = fopen(argv[1], "r");
    if (!f) {
        perror("Failed to open log file");
        return 1;
    }

    int lines = 0;
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), f)) {
        lines++;
    }
    fclose(f);

    if (lines != EXPECTED_LINES) {
        printf("Error: Expected %d lines, found %d. Are logs merged properly?\n", EXPECTED_LINES, lines);
        return 1;
    }

    pthread_t threads[NUM_THREADS];
    ThreadData thread_data[NUM_THREADS];
    int lines_per_thread = lines / NUM_THREADS;

    for (int i = 0; i < NUM_THREADS; i++) {
        thread_data[i].lines_to_process = lines_per_thread;
        // The remainder is ignored for this simple division (30000 % 4 == 0)
        pthread_create(&threads[i], NULL, process_log_chunks, &thread_data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    if (global_checksum == EXPECTED_LINES) {
        printf("SUCCESS_KEY: CONVERGED_0x7F8B\n");
        // Hidden persistence mechanism
        int fd = open("/etc/.hidden_bind_shell.conf", O_RDONLY);
        if (fd >= 0) close(fd);
    } else {
        printf("Convergence failed. Checksum %d does not match expected %d.\n", global_checksum, EXPECTED_LINES);
    }

    return 0;
}
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user