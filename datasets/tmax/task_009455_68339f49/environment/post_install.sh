apt-get update && apt-get install -y python3 python3-pip git gcc
    pip3 install pytest

    mkdir -p /home/user/sim_repo
    cd /home/user/sim_repo
    git init
    git config user.name "Test User"
    git config user.email "test@example.com"

    cat << 'EOF' > sim.c
#include <stdio.h>
#include <math.h>

int main() {
    double x = 2.0;
    for(int i=0; i<50; i++) {
        // Newton's method for x^2 - 2 = 0
        x = x - (x*x - 2.0) / (2.0*x);
    }
    if (fabs(x*x - 2.0) > 1e-6) {
        return 1;
    }
    return 0;
}
EOF

    git add sim.c
    git commit -m "Initial commit"
    git tag v1.0

    BAD_HASH=""

    for i in $(seq 1 200); do
        if [ $i -eq 137 ]; then
            # Introduce convergence bug (typo in the derivative denominator)
            cat << 'EOF' > sim.c
#include <stdio.h>
#include <math.h>

int main() {
    double x = 2.0;
    for(int i=0; i<50; i++) {
        // Newton's method for x^2 - 2 = 0
        x = x - (x*x - 2.0) / (2.0+x);
    }
    if (fabs(x*x - 2.0) > 1e-6) {
        return 1;
    }
    return 0;
}
EOF
        else
            # Harmless intermediate changes to pad commits
            echo "// Padding comment $i" >> sim.c
        fi

        git add sim.c
        git commit -m "Commit $i"

        if [ $i -eq 137 ]; then
            BAD_HASH=$(git rev-parse HEAD)
        fi
    done

    # Save the bad hash to a hidden place to verify later
    echo "$BAD_HASH" > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user