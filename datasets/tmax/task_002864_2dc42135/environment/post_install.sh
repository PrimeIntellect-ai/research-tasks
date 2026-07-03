apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest pandas numpy

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /app/legacy_score_predictor.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Error: Invalid number of arguments.\n");
        fprintf(stderr, "Usage: %s <feature_C_clean> <feature_F_imputed> <feature_J_log>\n", argv[0]);
        return 1;
    }
    double c = atof(argv[1]);
    double f = atof(argv[2]);
    double j = atof(argv[3]);

    double score = 2.5 * c + 1.2 * f - 0.8 * j + 5.0;
    printf("%f\n", score);
    return 0;
}
EOF

    gcc -O2 -s /app/legacy_score_predictor.c -o /app/legacy_score_predictor
    chmod +x /app/legacy_score_predictor
    rm /app/legacy_score_predictor.c

    cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

def generate_data(n_rows, filename, is_test=False):
    f_vals = np.random.uniform(0, 50, n_rows)
    # Add missing values to F (~10%)
    mask = np.random.rand(n_rows) < 0.1
    f_vals_with_nan = np.where(mask, np.nan, f_vals)

    data = {
        'A': np.random.randn(n_rows),
        'B': np.random.choice(['Red', 'Blue', 'Green'], n_rows),
        'C': ["${:,.2f}".format(x) for x in np.random.uniform(10, 1000, n_rows)],
        'D': np.random.randint(1, 100, n_rows),
        'E': np.random.randn(n_rows),
        'F': f_vals_with_nan,
        'G': np.random.choice(['X', 'Y', 'Z'], n_rows),
        'H': np.random.randn(n_rows),
        'I': np.random.randn(n_rows),
        'J': np.random.exponential(2.0, n_rows)
    }

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

    # Compute true scores exactly as the C binary would expect
    c_clean = df['C'].replace('[\$,]', '', regex=True).astype(float)
    f_imputed = df['F'].fillna(df['F'].mean())
    j_log = np.log1p(df['J'])

    scores = 2.5 * c_clean + 1.2 * f_imputed - 0.8 * j_log + 5.0
    return scores

generate_data(1000, '/home/user/train_data.csv')
test_scores = generate_data(500, '/home/user/test_data.csv', is_test=True)
test_scores.to_csv('/tmp/true_test_scores.csv', index=False, header=False)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    chmod -R 777 /home/user