apt-get update && apt-get install -y python3 python3-pip git gcc build-essential
    pip3 install pytest

    mkdir -p /home/user/signal_lib
    cd /home/user/signal_lib

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"
    git init

    cat << 'EOF' > signal_calc.c
#include <stdio.h>

double compute_series(int iterations) {
    double sum = 0.0;
    for (int i = 1; i <= iterations; i++) {
        sum += 1.0 / ((double)i * (double)i);
    }
    return sum;
}
EOF
    git add signal_calc.c && git commit -m "Initial commit"

    for i in $(seq 1 100); do
        if [ $i -eq 67 ]; then
            cat << 'EOF' > signal_calc.c
#include <stdio.h>

double compute_series(int iterations) {
    float sum = 0.0;
    for (int i = 1; i <= iterations; i++) {
        sum += (float)(1.0 / ((double)i * (double)i));
    }
    return (double)sum;
}
EOF
        else
            echo "// comment $i" >> signal_calc.c
        fi
        git add signal_calc.c
        git commit -m "Commit $i"
        if [ $i -eq 67 ]; then
            git rev-parse HEAD > /tmp/expected_bad_commit.txt
        fi
    done

    useradd -m -s /bin/bash user || true
    echo 'export CFLAGS="-ffast-math"' >> /home/user/.bashrc

    chmod -R 777 /home/user