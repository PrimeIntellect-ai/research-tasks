apt-get update && apt-get install -y python3 python3-pip git gcc make imagemagick
    pip3 install pytest

    mkdir -p /app

    # Generate the image
    convert -size 400x200 xc:white -fill red -pointsize 24 -draw "text 20,100 'SLA Threshold: 99.9995%'" /app/uptime_graph.png

    # Setup the git repository
    mkdir -p /home/user/uptime_repo/src
    cd /home/user/uptime_repo
    git init
    git config --global user.email "sre@example.com"
    git config --global user.name "SRE"

    # Makefile
    cat << 'EOF' > Makefile
all:
	mkdir -p build
	gcc -O2 src/uptime_calc.c -o build/uptime_calc
EOF

    # Good version (v1.0)
    cat << 'EOF' > src/uptime_calc.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    double sum = 0.0;
    double c = 0.0;
    double val;
    while (scanf("%lf", &val) == 1) {
        double y = val - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    printf("%.10f\n", sum);
    return 0;
}
EOF

    git add Makefile src/uptime_calc.c
    git commit -m "Initial commit with Kahan summation"
    git tag v1.0

    # Compile the oracle
    gcc -O2 src/uptime_calc.c -o /app/uptime_oracle
    strip /app/uptime_oracle
    chmod +x /app/uptime_oracle

    # Dummy commit 1
    echo "// dummy 1" >> src/uptime_calc.c
    git commit -am "Dummy commit 1"

    # Regression commit
    cat << 'EOF' > src/uptime_calc.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    float sum = 0.0f;
    float val;
    while (scanf("%f", &val) == 1) {
        sum += val;
    }
    printf("%.10f\n", (double)sum);
    return 0;
}
EOF
    git commit -am "Refactor accumulation loop"

    # Dummy commit 2
    echo "// dummy 2" >> src/uptime_calc.c
    git commit -am "Dummy commit 2"

    # Dummy commit 3
    echo "// dummy 3" >> src/uptime_calc.c
    git commit -am "Dummy commit 3"

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app