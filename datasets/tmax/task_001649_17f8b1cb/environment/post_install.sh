apt-get update && apt-get install -y python3 python3-pip git gcc make
pip3 install pytest

useradd -m -s /bin/bash user || true

git config --global user.email "test@example.com"
git config --global user.name "Test User"

mkdir -p /home/user/job_queue
cd /home/user/job_queue
git init

# Create the initial working version
cat << 'EOF' > queue.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define MAX_JOBS 10

int jobs[MAX_JOBS];
int head = 0;
int tail = 0;
int count = 0;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

void push_job(int job_id) {
    pthread_mutex_lock(&lock);
    while (count == MAX_JOBS) {
        pthread_cond_wait(&cond, &lock);
    }
    jobs[tail] = job_id;
    tail = (tail + 1) % MAX_JOBS;
    count++;
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
}

int pop_all_jobs() {
    pthread_mutex_lock(&lock);
    int processed = 0;
    int i = head;

    // Process all currently available jobs
    while (i != tail) {
        processed++;
        i = (i + 1) % MAX_JOBS;
    }

    head = tail;
    count = 0;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&lock);

    return processed;
}

void* producer(void* arg) {
    for (int i = 0; i < 50; i++) {
        push_job(i);
    }
    return NULL;
}

void* consumer(void* arg) {
    int total = 0;
    while (total < 100) {
        total += pop_all_jobs();
        usleep(1000);
    }
    return NULL;
}

int main() {
    pthread_t p1, p2, c1;
    pthread_create(&p1, NULL, producer, NULL);
    pthread_create(&p2, NULL, producer, NULL);
    pthread_create(&c1, NULL, consumer, NULL);

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);
    pthread_join(c1, NULL);

    printf("Success\n");
    return 0;
}
EOF

cat << 'EOF' > test.sh
#!/bin/bash
gcc -O0 -g -pthread queue.c -o queue
timeout 3s ./queue
exit $?
EOF
chmod +x test.sh

git add queue.c test.sh
git commit -m "Initial working version"
git tag v1.0

# Good commit 2
echo "// Refactoring comments" >> queue.c
git commit -am "Add comments"

# BAD COMMIT: Introduce the off-by-one infinite loop
sed -i 's/i = (i + 1) % MAX_JOBS;/i = (i + 1) % (MAX_JOBS + 1);/' queue.c
git commit -am "Optimize loop modulo arithmetic"
BAD_COMMIT=$(git rev-parse HEAD)

# Bad commit 4
echo "// More comments" >> queue.c
git commit -am "Add more comments"

# Bad commit 5
cat << 'EOF' > Makefile
all:
	gcc -O0 -g -pthread queue.c -o queue
EOF
git add Makefile
git commit -m "Add Makefile"

# Save the expected bad commit hash to a hidden location for validation
echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

chmod -R 777 /home/user