apt-get update && apt-get install -y python3 python3-pip imagemagick tesseract-ocr libtesseract-dev gcc make
    pip3 install pytest

    mkdir -p /home/user/aggregator
    mkdir -p /app

    # Create the legacy_doc.png fixture
    convert -size 800x400 xc:white -font DejaVu-Sans -pointsize 18 -fill black \
      -draw "text 20,40 'CRITICAL ARCHITECTURE NOTES'" \
      -draw "text 20,80 'LOCKING PROTOCOL:'" \
      -draw "text 20,110 'To prevent circular wait deadlocks, threads MUST acquire'" \
      -draw "text 20,140 'IN_Q_LOCK before OUT_Q_LOCK.'" \
      -draw "text 20,190 'SERIALIZATION PROTOCOL:'" \
      -draw "text 20,220 '1. Magic Header: 4 bytes -> 0xCAFEBABE'" \
      -draw "text 20,250 '2. Payload Length: 2 bytes, Big Endian'" \
      -draw "text 20,280 '3. Payload: Raw ASCII bytes'" \
      /app/legacy_doc.png

    # Generate Oracle source code and compile it
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <arpa/inet.h>

void serialize_and_write(const char *payload) {
    uint32_t magic = htonl(0xCAFEBABE);
    uint16_t len = htons((uint16_t)strlen(payload));
    fwrite(&magic, sizeof(magic), 1, stdout);
    fwrite(&len, sizeof(len), 1, stdout);
    fwrite(payload, 1, strlen(payload), stdout);
}

int main() {
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    while ((read = getline(&line, &len, stdin)) != -1) {
        if (read > 0 && line[read-1] == '\n') {
            line[read-1] = '\0';
        }
        serialize_and_write(line);
    }
    free(line);
    return 0;
}
EOF
    gcc -O2 /tmp/oracle.c -o /app/oracle_aggregator
    chmod +x /app/oracle_aggregator

    # Create Buggy Workspace
    cat << 'EOF' > /home/user/aggregator/main.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

extern void* worker_thread(void* arg);
extern void serialize_event(const char* payload);

pthread_mutex_t IN_Q_LOCK = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t OUT_Q_LOCK = PTHREAD_MUTEX_INITIALIZER;

#define MAX_QUEUE 1024
char* in_queue[MAX_QUEUE];
int in_head = 0, in_tail = 0;

int main() {
    pthread_t workers[4];
    for (int i = 0; i < 4; i++) {
        pthread_create(&workers[i], NULL, worker_thread, NULL);
    }

    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    // Read stdin and push to in_queue
    while ((read = getline(&line, &len, stdin)) != -1) {
        if (read > 0 && line[read-1] == '\n') line[read-1] = '\0';

        // Simulating the buggy main thread acquiring OUT before IN occasionally
        pthread_mutex_lock(&OUT_Q_LOCK);
        pthread_mutex_lock(&IN_Q_LOCK);

        in_queue[in_head] = strdup(line);
        in_head = (in_head + 1) % MAX_QUEUE;

        pthread_mutex_unlock(&IN_Q_LOCK);
        pthread_mutex_unlock(&OUT_Q_LOCK);
    }

    exit(0);
}
EOF

    cat << 'EOF' > /home/user/aggregator/worker.c
#include <pthread.h>
#include <stdio.h>

extern pthread_mutex_t IN_Q_LOCK;
extern pthread_mutex_t OUT_Q_LOCK;

void* worker_thread(void* arg) {
    while(1) {
        // BUG: Acquires OUT_Q_LOCK before IN_Q_LOCK causing deadlock
        pthread_mutex_lock(&OUT_Q_LOCK);
        pthread_mutex_lock(&IN_Q_LOCK);

        // Process event...

        pthread_mutex_unlock(&IN_Q_LOCK);
        pthread_mutex_unlock(&OUT_Q_LOCK);
    }
    return NULL;
}
EOF

    cat << 'EOF' > /home/user/aggregator/serialize.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

void serialize_event(const char* payload) {
    // BUG: Wrong magic bytes, wrong endianness
    uint32_t magic = 0xCAFEF00D; 
    uint16_t len = (uint16_t)strlen(payload);

    fwrite(&magic, sizeof(magic), 1, stdout);
    fwrite(&len, sizeof(len), 1, stdout);
    fwrite(payload, 1, strlen(payload), stdout);
}
EOF

    cat << 'EOF' > /home/user/aggregator/Makefile
all:
	gcc main.c worker.c serialize.c -o aggregator
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/aggregator
    chmod -R 777 /home/user