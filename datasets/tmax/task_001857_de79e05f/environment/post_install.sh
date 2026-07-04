apt-get update && apt-get install -y python3 python3-pip gcc make git gdb
    pip3 install pytest

    mkdir -p /app/smhasher
    cd /app/smhasher
    git init
    git config user.email "author@example.com"
    git config user.name "Author"

    cat << 'EOF' > murmur3.h
#include <stdint.h>
#include <stddef.h>
void MurmurHash3_x86_32(const void *key, int len, uint32_t seed, void *out);
EOF

    cat << 'EOF' > murmur3.c
#include "murmur3.h"
static inline uint32_t rotl32 ( uint32_t x, int8_t r ) {
  return (x << r) | (x >> (32 - r));
}
void MurmurHash3_x86_32(const void *key, int len, uint32_t seed, void *out) {
  const uint8_t * data = (const uint8_t*)key;
  const int nblocks = len / 4;
  uint32_t h1 = seed;
  const uint32_t c1 = 0xcc9e2d51;
  const uint32_t c2 = 0x1b873593;
  const uint32_t * blocks = (const uint32_t *)(data + nblocks*4);
  for(int i = -nblocks; i; i++) {
    uint32_t k1 = blocks[i];
    k1 *= c1; k1 = rotl32(k1,15); k1 *= c2;
    h1 ^= k1; h1 = rotl32(h1,13); h1 = h1*5+0xe6546b64;
  }
  const uint8_t * tail = (const uint8_t*)(data + nblocks*4);
  int32_t k1 = 0;
  switch(len & 3) {
    case 3: k1 ^= tail[2] << 16;
    case 2: k1 ^= tail[1] << 8;
    case 1: k1 ^= tail[0];
            k1 *= c1; k1 = rotl32(k1,15); k1 *= c2; h1 ^= k1;
  };
  h1 ^= len; h1 ^= h1 >> 16; h1 *= 0x85ebca6b; h1 ^= h1 >> 13; h1 *= 0xc2b2ae35; h1 ^= h1 >> 16;
  *(uint32_t*)out = h1;
}
EOF

    cat << 'EOF' > parallel_hash.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "murmur3.h"

pthread_mutex_t mutex_A = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_B = PTHREAD_MUTEX_INITIALIZER;

void* thread1_func(void* arg) {
    pthread_mutex_lock(&mutex_A);
    usleep(1000);
    pthread_mutex_lock(&mutex_B);
    pthread_mutex_unlock(&mutex_B);
    pthread_mutex_unlock(&mutex_A);
    return NULL;
}

void* thread2_func(void* arg) {
    pthread_mutex_lock(&mutex_A);
    usleep(1000);
    pthread_mutex_lock(&mutex_B);
    pthread_mutex_unlock(&mutex_B);
    pthread_mutex_unlock(&mutex_A);
    return NULL;
}

int main() {
    char buffer[8192];
    size_t len = fread(buffer, 1, sizeof(buffer), stdin);
    pthread_t t1, t2;
    pthread_create(&t1, NULL, thread1_func, NULL);
    pthread_create(&t2, NULL, thread2_func, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    uint32_t out;
    MurmurHash3_x86_32(buffer, len, 0, &out);
    printf("%08x\n", out);
    return 0;
}
EOF

    cat << 'EOF' > Makefile
all: fixed_hash
fixed_hash: parallel_hash.o murmur3.o
	gcc -o fixed_hash parallel_hash.o murmur3.o -pthread
parallel_hash.o: parallel_hash.c
	gcc -c parallel_hash.c
murmur3.o: murmur3.c
	gcc -c murmur3.c
clean:
	rm -f *.o fixed_hash
EOF

    git add .
    git commit -m "Initial commit"

    sed -i 's/int32_t k1 = 0;/uint32_t k1 = 0;/g' murmur3.c
    git add murmur3.c
    git commit -m "Fix numerical instability in finalization step"

    make
    mkdir -p /opt/oracle
    cp fixed_hash /opt/oracle/hash_oracle
    make clean

    echo "// Some comment" >> murmur3.h
    git add murmur3.h
    git commit -m "Add comment"

    echo "// Another comment" >> murmur3.h
    git add murmur3.h
    git commit -m "Add another comment"

    git revert --no-edit HEAD~2

    cat << 'EOF' > parallel_hash.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "murmur3.h"

pthread_mutex_t mutex_A = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_B = PTHREAD_MUTEX_INITIALIZER;

void* thread1_func(void* arg) {
    pthread_mutex_lock(&mutex_A);
    usleep(1000);
    pthread_mutex_lock(&mutex_B);
    pthread_mutex_unlock(&mutex_B);
    pthread_mutex_unlock(&mutex_A);
    return NULL;
}

void* thread2_func(void* arg) {
    pthread_mutex_lock(&mutex_B);
    usleep(1000);
    pthread_mutex_lock(&mutex_A);
    pthread_mutex_unlock(&mutex_A);
    pthread_mutex_unlock(&mutex_B);
    return NULL;
}

int main() {
    char buffer[8192];
    size_t len = fread(buffer, 1, sizeof(buffer), stdin);
    pthread_t t1, t2;
    pthread_create(&t1, NULL, thread1_func, NULL);
    pthread_create(&t2, NULL, thread2_func, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    uint32_t out;
    MurmurHash3_x86_32(buffer, len, 0, &out);
    printf("%08x\n", out);
    return 0;
}
EOF
    git add parallel_hash.c
    git commit -m "Update wrapper"

    cat << 'EOF' > Makefile
all: murmur3_fuzzer
murmur3_fuzzer: parallell_hash.o murmur3.o
	gcc -o murmur3_fuzzer parallel_hash.o murmur3.o
parallell_hash.o: parallel_hash.c
	gcc -c parallel_hash.c
murmur3.o: murmur3.c
	gcc -c murmur3.c
clean:
	rm -f *.o murmur3_fuzzer
EOF
    git add Makefile
    git commit -m "Update Makefile"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user