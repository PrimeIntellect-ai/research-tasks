apt-get update && apt-get install -y python3 python3-pip gcc procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/memory_tracker.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
// #include <assert.h> // Intentionally omitted for the agent to potentially add

int main() {
    FILE *log = fopen("/home/user/alloc.log", "w");
    if (!log) return 1;

    for (int i = 1; i <= 50; i++) {
        void *ptr = malloc(128);
        fprintf(log, "ALLOC %d %p\n", i, ptr);
        fflush(log);

        // Bug: leaks when i is a multiple of 7
        if (i % 7 != 0) { 
            fprintf(log, "FREE %d %p\n", i, ptr);
            fflush(log);
            free(ptr);
        }
    }

    // Keep running to hold the FD open
    while(1) { sleep(1); } 
    return 0;
}
EOF

    gcc /home/user/memory_tracker.c -o /home/user/memory_tracker

    # Note: The background process is not started here in %post, 
    # as it would cause the build to hang. The evaluation platform
    # is responsible for running the background setup script.

    chmod -R 777 /home/user