apt-get update && apt-get install -y python3 python3-pip git build-essential clang llvm
pip3 install pytest

mkdir -p /home/user/trajectory_calc
cd /home/user/trajectory_calc

git init
git config user.name "Test User"
git config user.email "test@example.com"

# 1. Initial good commit
cat << 'EOF' > trajectory.h
#ifndef TRAJECTORY_H
#define TRAJECTORY_H
double calc_y(double v0_y, double t);
#endif
EOF

cat << 'EOF' > trajectory.c
#include "trajectory.h"

double calc_y(double v0_y, double t) {
    double g = 9.8;
    return v0_y * t - 0.5 * g * t * t;
}
EOF

cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-Wall -Wextra -O2

all: trajectory.o

trajectory.o: trajectory.c
	$(CC) $(CFLAGS) -c trajectory.c -o trajectory.o

clean:
	rm -f *.o fuzzer
EOF

git add trajectory.h trajectory.c Makefile
git commit -m "Initial commit: working trajectory calc"
git tag v1.0

# 2. Add some comments (Good)
echo "// Helper library for physics simulation" >> trajectory.h
git commit -am "Add docs to header"

# 3. Add a helper macro (Good)
echo "#define GRAVITY 9.8" >> trajectory.h
git commit -am "Define gravity macro"

# 4. THE BAD COMMIT (Introduces build failure due to invalid float XOR)
cat << 'EOF' > trajectory.c
#include "trajectory.h"

double calc_y(double v0_y, double t) {
    // Optimized formula
    return v0_y * t - (GRAVITY * t ^ 2) / 2.0;
}
EOF
git commit -am "Optimize y calculation formula"
BAD_COMMIT=$(git rev-parse HEAD)

# 5. Unrelated commit (Bad, inherits previous error)
echo "// TODO: add drag" >> trajectory.h
git commit -am "Add todo"

# 6. Another unrelated commit (Bad)
echo "test:" >> Makefile
echo "	\$(CC) \$(CFLAGS) trajectory.c -c" >> Makefile
git commit -am "Update makefile"

# Store the expected bad commit in a hidden root location for the verification script
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/trajectory_calc
chmod -R 777 /home/user