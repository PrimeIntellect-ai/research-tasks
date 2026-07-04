apt-get update && apt-get install -y python3 python3-pip gcc make sqlite3
    pip3 install pytest

    # Phase 1: Vendored Package
    mkdir -p /app/tinyexpr

    cat << 'EOF' > /app/tinyexpr/tinyexpr.c
#include <math.h>
double te_interp(const char* expr, int* error) {
    return 0.0;
}
EOF

    cat << 'EOF' > /app/tinyexpr/test.c
#include <assert.h>
#include <stdio.h>
#include <math.h>

int main() {
    double x = NAN;
    assert(isnan(x) && "Precision/NaN assertion failed");
    printf("Tests passed!\n");
    return 0;
}
EOF

    cat << 'EOF' > /app/tinyexpr/Makefile
CC = gcc
CFLAGS += -O3 -ffast-math

all: tinyexpr.o

tinyexpr.o: tinyexpr.c
	$(CC) $(CFLAGS) -c tinyexpr.c

test: tinyexpr.o
	$(CC) $(CFLAGS) test.c tinyexpr.o -o test_runner -lm
	./test_runner
EOF

    # Phase 2: Database Setup
    mkdir -p /app/data
    cat << 'EOF' > /tmp/make_db.py
import sqlite3
import os
import signal

conn = sqlite3.connect('/app/data/formulas.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('CREATE TABLE clean_formulas (expression TEXT)')
conn.execute('CREATE TABLE evil_formulas (expression TEXT)')
conn.execute('INSERT INTO clean_formulas VALUES ("3.14 * 2.0"), ("sin(1)"), ("sqrt(4)")')
conn.execute('INSERT INTO evil_formulas VALUES ("1/0"), ("0/0"), ("log(-1)"), ("1e999 * 1e999")')
conn.commit()

# Force exit without cleanup to preserve WAL file
os.kill(os.getpid(), signal.SIGKILL)
EOF
    python3 /tmp/make_db.py || true

    # Corrupt the main database file
    dd if=/dev/zero of=/app/data/formulas.db bs=100 count=1 conv=notrunc

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user