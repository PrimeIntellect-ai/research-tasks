apt-get update && apt-get install -y python3 python3-pip git build-essential
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/ticket_7384_repo
cd /home/user/ticket_7384_repo
git init
git config --global user.email "test@example.com"
git config --global user.name "Test User"

cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-Wall -Wextra -O2
LDFLAGS=-lm

all: calc_engine test_runner

calc_engine: main.c solver.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

test_runner: test.c solver.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

test: test_runner
	./test_runner

clean:
	rm -f calc_engine test_runner
EOF

cat << 'EOF' > solver.h
#ifndef SOLVER_H
#define SOLVER_H

double custom_sqrt(double x);
double sum_array(double *arr, int n);

#endif
EOF

cat << 'EOF' > solver.c
#include "solver.h"
#include <math.h>

double custom_sqrt(double x) {
    if (x < 0) return -1.0;
    if (x == 0) return 0;
    double guess = x / 2.0;
    double tol = 1e-9;
    int max_iter = 1000;
    for (int i = 0; i < max_iter; i++) {
        double diff = guess * guess - x;
        if (fabs(diff) < tol) {
            return guess;
        }
        guess = guess - diff / (2.0 * guess);
    }
    return -1.0; // Convergence failure
}

double sum_array(double *arr, int n) {
    double sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
EOF

cat << 'EOF' > main.c
#include <stdio.h>
#include "solver.h"

int main() {
    printf("Result: %f\n", custom_sqrt(25.0));
    return 0;
}
EOF

cat << 'EOF' > test.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "solver.h"

int main() {
    int failed = 0;

    // Test 1: Convergence and Precision
    double sq = custom_sqrt(2.0);
    if (fabs(sq - 1.41421356) > 1e-5) {
        printf("Test 1 Failed: custom_sqrt(2.0) = %f\n", sq);
        failed = 1;
    }

    // Test 2: Array bounds (Checking for memory corruption or wrong sum)
    double *arr = malloc(5 * sizeof(double));
    for(int i=0; i<5; i++) arr[i] = 1.0;

    // Place a poison pill right after the array
    double *poison = malloc(sizeof(double));
    *poison = 9999.0;

    double s = sum_array(arr, 5);
    if (s != 5.0) {
        printf("Test 2 Failed: sum_array returned %f, expected 5.0\n", s);
        failed = 1;
    }

    free(arr);
    free(poison);

    if (failed) {
        return 1;
    }
    printf("All tests passed!\n");
    return 0;
}
EOF

git add Makefile solver.h solver.c main.c test.c
git commit -m "Initial working commit"
git tag v1.0

# Commit 2: Break Linker
sed -i 's/LDFLAGS=-lm/LDFLAGS=/' Makefile
git add Makefile
git commit -m "Refactor Makefile"

# Commit 3: Break boundary condition (Off-by-one)
sed -i 's/i < n/i <= n/' solver.c
git add solver.c
git commit -m "Update array processing loop"

# Commit 4: Break convergence/precision
sed -i 's/double guess =/float guess =/' solver.c
git add solver.c
git commit -m "Optimize solver memory usage"
git rev-parse HEAD > /tmp/expected_hash.txt

# Commit 5: Add README
echo "# Calc Engine" > README.md
git add README.md
git commit -m "Add README"

chmod -R 777 /home/user