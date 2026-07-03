apt-get update && apt-get install -y python3 python3-pip git gcc make
pip3 install pytest

mkdir -p /home/user/math_sim
cd /home/user/math_sim
git init

git config user.name "Test User"
git config user.email "test@example.com"

cat << 'EOF' > sim.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    int n = atoi(argv[1]);
    double sum = 0;
    int* arr = malloc(n * sizeof(int));
    for(int i=0; i<n; i++) arr[i] = i;

    for(int i=0; i<n; i++) {
#ifdef CRASH
        if (i == n-1) arr[n+10000] = 0; 
#endif
        sum += sin(arr[i]);
    }
    printf("%f\n", sum);
    free(arr);
    return 0;
}
EOF

cat << 'EOF' > Makefile
all:
	gcc sim.c -lm -o sim
clean:
	rm -f sim
EOF

git add sim.c Makefile
git commit -m "Initial commit"
git tag v1.0

for i in $(seq 1 200); do
    echo "// comment $i" >> sim.c
    if [ $i -eq 50 ]; then
        sed -i 's/-lm//' Makefile
    fi
    if [ $i -eq 120 ]; then
        sed -i 's/#ifdef CRASH/#define CRASH\n#ifdef CRASH/' sim.c
    fi
    if [ $i -eq 170 ]; then
        sed -i 's/gcc sim.c -o sim/gcc sim.c -lm -o sim/' Makefile
    fi
    git add sim.c Makefile
    git commit -m "Commit $i"
    if [ $i -eq 120 ]; then
        BAD_COMMIT=$(git rev-parse HEAD)
    fi
done

echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/math_sim
chmod -R 777 /home/user