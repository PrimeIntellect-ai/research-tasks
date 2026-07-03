apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest numpy pandas matplotlib

    mkdir -p /home/user/workspace
    cd /home/user/workspace

    # 1. Create the C source file calc_peaks.c
    cat << 'EOF' > calc_peaks.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_NODES 100

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <edges_file>\n", argv[0]);
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int degrees[MAX_NODES] = {0};
    int u, v;
    int max_node = 0;
    while (fscanf(f, "%d %d", &u, &v) == 2) {
        degrees[u]++;
        degrees[v]++;
        if (u > max_node) max_node = u;
        if (v > max_node) max_node = v;
    }
    fclose(f);

    int unique_degrees[MAX_NODES];
    int ud_count = 0;
    for (int i = 0; i <= max_node; i++) {
        if (degrees[i] > 0) {
            int found = 0;
            for (int j = 0; j < ud_count; j++) {
                if (unique_degrees[j] == degrees[i]) {
                    found = 1; break;
                }
            }
            if (!found) unique_degrees[ud_count++] = degrees[i];
        }
    }

    // Sort descending manually
    for (int i = 0; i < ud_count - 1; i++) {
        for (int j = i + 1; j < ud_count; j++) {
            if (unique_degrees[i] < unique_degrees[j]) {
                int temp = unique_degrees[i];
                unique_degrees[i] = unique_degrees[j];
                unique_degrees[j] = temp;
            }
        }
    }

    printf("Theoretical peaks:\n");
    for (int i = 0; i < (ud_count < 3 ? ud_count : 3); i++) {
        printf("%.2f\n", unique_degrees[i] * 314.15);
    }
    return 0;
}
EOF

    # 2. Create the molecule.edges file
    cat << 'EOF' > molecule.edges
0 1
0 2
0 3
1 4
1 5
1 6
1 7
2 8
2 9
2 10
2 11
2 12
EOF

    # 3. Create a python script to generate spectrum.csv with noise
    cat << 'EOF' > gen_data.py
import numpy as np
import pandas as pd

np.random.seed(42)
wavenumbers = np.linspace(500, 2500, 1000)

def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 / wid)

# Actual experimental peaks will be slightly shifted from theoretical
intensity = (
    gaussian(wavenumbers, 100, 940.0, 500) +
    gaussian(wavenumbers, 150, 1572.0, 400) +
    gaussian(wavenumbers, 120, 1880.0, 600)
)
# Add some noise
noise = np.random.normal(0, 5, len(wavenumbers))
intensity += noise

df = pd.DataFrame({'Wavenumber': wavenumbers, 'Intensity': intensity})
df.to_csv('spectrum.csv', index=False)
EOF
    python3 gen_data.py
    rm gen_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user