apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev binutils
pip3 install pytest numpy matplotlib

mkdir -p /app
mkdir -p /home/user

cat << 'EOF' > /app/weights.csv
token,v1,v2,v3
error,1.2,-0.4,0.8
fail,-0.5,1.5,0.1
warning,0.1,0.1,0.1
system,0.0,0.5,-0.2
user,0.3,0.3,0.3
EOF

cat << 'EOF' > /home/user/plot_anomalies.py
import matplotlib
import matplotlib.pyplot as plt
import subprocess
import random

# Bug: wrong backend or not saving properly
# The agent should add matplotlib.use('Agg') or ensure plt.savefig is used correctly.
logs = ["error system", "user warning", "unknown token", "fail system error"]
scores = []
for log in logs:
    result = subprocess.run(["/app/legacy_scorer"], input=log.encode(), capture_output=True)
    scores.append(float(result.stdout.decode().strip()))

plt.hist(scores)
# The bug is that savefig is called after show() or figure is cleared, or backend issues.
plt.show()
plt.savefig('/home/user/plot.png')
EOF

cat << 'EOF' > /tmp/legacy_scorer.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main() {
    char line[1024];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    line[strcspn(line, "\n")] = 0;

    double sum_x = 0, sum_y = 0, sum_z = 0;
    char *token = strtok(line, " ");

    while (token != NULL) {
        double v1 = 0.5, v2 = 0.5, v3 = 0.5;
        if (strcmp(token, "error") == 0) { v1=1.2; v2=-0.4; v3=0.8; }
        else if (strcmp(token, "fail") == 0) { v1=-0.5; v2=1.5; v3=0.1; }
        else if (strcmp(token, "warning") == 0) { v1=0.1; v2=0.1; v3=0.1; }
        else if (strcmp(token, "system") == 0) { v1=0.0; v2=0.5; v3=-0.2; }
        else if (strcmp(token, "user") == 0) { v1=0.3; v2=0.3; v3=0.3; }

        sum_x += v1;
        sum_y += v2;
        sum_z += v3;

        token = strtok(NULL, " ");
    }

    double norm = sqrt(sum_x*sum_x + sum_y*sum_y + sum_z*sum_z);
    printf("%.4f\n", norm * 0.85);
    return 0;
}
EOF

gcc -O2 /tmp/legacy_scorer.c -o /app/legacy_scorer -lm
strip /app/legacy_scorer
rm /tmp/legacy_scorer.c

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user
chmod -R 777 /app