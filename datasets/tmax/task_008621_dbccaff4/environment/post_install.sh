apt-get update && apt-get install -y python3 python3-pip git gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/metrics-daemon
    cd /home/user/metrics-daemon
    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    # Create initial code
    cat << 'EOF' > Makefile
all: metrics-daemon
metrics-daemon: main.c parser.c queue.c
	gcc -g -pthread -Wall -o metrics-daemon main.c parser.c queue.c
clean:
	rm -f metrics-daemon
EOF

    cat << 'EOF' > queue.h
#ifndef QUEUE_H
#define QUEUE_H
void enqueue(char* metric);
int get_queue_length();
#endif
EOF

    cat << 'EOF' > parser.h
#ifndef PARSER_H
#define PARSER_H
char* parse_metric(const char* input);
#endif
EOF

    cat << 'EOF' > queue.c
#include <stdlib.h>
#include <pthread.h>
#include "queue.h"

typedef struct Node {
    char* data;
    struct Node* next;
} Node;

Node* head = NULL;
Node* tail = NULL;
int count = 0;
pthread_mutex_t q_mutex = PTHREAD_MUTEX_INITIALIZER;

void enqueue(char* metric) {
    Node* n = malloc(sizeof(Node));
    n->data = metric;
    n->next = NULL;

    pthread_mutex_lock(&q_mutex);
    if (!head) {
        head = n;
        tail = n;
    } else {
        tail->next = n;
        tail = n;
    }
    count++;
    pthread_mutex_unlock(&q_mutex);
}

int get_queue_length() {
    return count;
}
EOF

    cat << 'EOF' > parser.c
#include <string.h>
#include <stdlib.h>
#include "parser.h"

char* parse_metric(const char* input) {
    char* buf = strdup(input);
    if (!buf) return NULL;

    if (strncmp(buf, "METRIC:", 7) == 0) {
        return buf;
    }

    free(buf);
    return NULL;
}
EOF

    cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include "parser.h"
#include "queue.h"

int main(int argc, char** argv) {
    // Simple mock main
    return 0;
}
EOF

    git add Makefile queue.h parser.h queue.c parser.c main.c
    git commit -m "Initial commit: basic daemon structure"

    # COMMIT 2: Introduce memory leak
    cat << 'EOF' > parser.c
#include <string.h>
#include <stdlib.h>
#include "parser.h"

char* parse_metric(const char* input) {
    char* buf = strdup(input);
    if (!buf) return NULL;

    // Check for advanced format
    if (strstr(buf, "INVALID_CHARS")) {
        // BUG: Memory leak introduced here
        return NULL;
    }

    if (strncmp(buf, "METRIC:", 7) == 0) {
        return buf;
    }

    free(buf);
    return NULL;
}
EOF
    git add parser.c
    git commit -m "Add validation for invalid characters in parser"
    LEAK_COMMIT=$(git rev-parse HEAD)
    echo $LEAK_COMMIT > /tmp/expected_leak_commit.txt

    # COMMIT 3: Add bad payload
    echo "METRIC:CPU_USAGE INVALID_CHARS" > bad_payload.txt
    git add bad_payload.txt
    git commit -m "Add test payload that causes OOM"

    # COMMIT 4: Introduce race condition
    cat << 'EOF' > queue.c
#include <stdlib.h>
#include <pthread.h>
#include "queue.h"

typedef struct Node {
    char* data;
    struct Node* next;
} Node;

Node* head = NULL;
Node* tail = NULL;
int count = 0;
pthread_mutex_t q_mutex = PTHREAD_MUTEX_INITIALIZER;

void enqueue(char* metric) {
    Node* n = malloc(sizeof(Node));
    n->data = metric;
    n->next = NULL;

    // BUG: Missing mutex lock around list operations
    if (!head) {
        head = n;
        tail = n;
    } else {
        tail->next = n;
        tail = n;
    }
    count++;
}

int get_queue_length() {
    return count;
}
EOF
    git add queue.c
    git commit -m "Optimize queue operations by adjusting locks"

    # COMMIT 5: Delete payload
    git rm bad_payload.txt
    git commit -m "Clean up unused test files"

    chown -R user:user /home/user/metrics-daemon
    chmod -R 777 /home/user