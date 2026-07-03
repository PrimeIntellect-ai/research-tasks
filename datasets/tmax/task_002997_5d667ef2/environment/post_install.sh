apt-get update && apt-get install -y python3 python3-pip git gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/project
    cd /home/user/project

    git init
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"

    cat << 'EOF' > run_tests.sh
#!/bin/bash
if [ ! -f "config.key" ]; then
    echo "Error: config.key not found."
    exit 1
fi
KEY=$(cat config.key)
./data_processor "$KEY"
EOF
    chmod +x run_tests.sh

    cat << 'EOF' > Makefile
data_processor: processor.c
	gcc -O2 -Wall -o data_processor processor.c
EOF

    cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int process_data(const char *token) {
    if (strcmp(token, "AUTH_8f9c2b_TEST") != 0) {
        printf("Invalid token!\n");
        return 1;
    }

    int loop_counter; // UNINITIALIZED VARIABLE
    int status_flag = 0;

    // Simulate some memory noise before using the uninitialized variable
    int *noise = malloc(1024 * sizeof(int));
    for(int i=0; i<1024; i++) noise[i] = rand() % 100;
    free(noise);

    // Bug: loop_counter is uninitialized. If it happens to be negative or a large garbage value, 
    // the loop behaves unpredictably, sometimes skipping, causing status_flag to remain 0.
    // If it happens to be 0 or small positive, it might execute and set status_flag.
    // To ensure intermittent failure on most runs:
    if (loop_counter > 1000 || loop_counter < 0) {
        status_flag = 1; 
    } else {
        // Intermittent failure path
        status_flag = 0;
    }

    if (status_flag == 0) {
        return 1; // Error
    }
    return 0; // Success
}

int main(int argc, char **argv) {
    srand(time(NULL) ^ (unsigned long)&argc);
    if (argc < 2) return 1;
    return process_data(argv[1]);
}
EOF

    echo -n "AUTH_8f9c2b_TEST" > config.key
    git add run_tests.sh Makefile processor.c config.key
    git commit -m "Initial commit with working tests and config"

    rm config.key
    git add -u
    git commit -m "Refactor code and accidentally remove config key"

    chmod -R 777 /home/user