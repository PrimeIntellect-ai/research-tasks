apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest numpy pandas scikit-learn joblib scipy

    mkdir -p /app/data /app/bin

    # Generate unlabeled_features.csv
    python3 -c "
import numpy as np
import pandas as pd
np.random.seed(42)
X = np.random.randn(10000, 20)
cols = [f'f{i}' for i in range(20)]
df = pd.DataFrame(X, columns=cols)
df.to_csv('/app/data/unlabeled_features.csv', index=False)
"

    # Create and compile the legacy scorer
    cat << 'EOF' > /tmp/scorer.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <csv_file>\n", argv[0]);
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Error opening file");
        return 1;
    }
    char line[4096];
    while (fgets(line, sizeof(line), file)) {
        double f[20];
        char *token = strtok(line, ",");
        int i = 0;
        while (token && i < 20) {
            f[i++] = atof(token);
            token = strtok(NULL, ",");
        }
        if (i >= 19) {
            double score = 4.5 * f[3] - 2.1 * f[8] + 3.8 * f[14] + 1.2 * f[18] + sin(f[0]);
            printf("%f\n", score);
        }
    }
    fclose(file);
    return 0;
}
EOF

    gcc -O3 /tmp/scorer.c -o /app/bin/scorer -lm
    strip -s /app/bin/scorer
    rm /tmp/scorer.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user