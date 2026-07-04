apt-get update && apt-get install -y python3 python3-pip gcc libhdf5-dev
    pip3 install pytest numpy scipy h5py matplotlib biopython

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/simulate_experiment.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
    FILE *f = fopen("experimental_data.csv", "w");
    if (!f) return 1;
    fprintf(f, "time,concentration\n");

    double k1 = 2.5; // Derived from FASTA length 250
    double k2 = 0.8; // Target value the agent should find

    // Exact solution for A(t):
    // A(t) = (100 / (k1 + k2)) * (k2 + k1 * exp(-(k1+k2)*t))

    for (int i = 0; i <= 50; i++) {
        double t = i * 0.2;
        double exact_A = (100.0 / (k1 + k2)) * (k2 + k1 * exp(-(k1 + k2) * t));
        // Add pseudo-random noise
        double noise = ((i * 13) % 11 - 5) * 0.1; 
        fprintf(f, "%.2f,%.4f\n", t, exact_A + noise);
    }

    fclose(f);
    return 0;
}
EOF

    python3 -c '
fasta_content = ">seq1 fictitious enzyme\n" + "M" * 250 + "\n"
with open("/home/user/enzyme.fasta", "w") as f:
    f.write(fasta_content)
'

    cat << 'EOF' > /home/user/fit_kinetics.py
import numpy as np
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# TODO: Read data from experimental_data.h5
# time_data = ...
# conc_data = ...

# TODO: Set k1 derived from FASTA
k1 = 0.0 

def euler_integrate(k2, t_eval):
    # Buggy, diverging Euler integrator with large fixed step
    dt = 2.0 
    t = 0.0
    A = 100.0
    B = 0.0

    results = []
    for target_t in t_eval:
        while t < target_t:
            dA = -k1 * A + k2 * B
            dB = k1 * A - k2 * B
            A += dA * dt
            B += dB * dt
            t += dt
        results.append(A)
    return np.array(results)

def model_wrapper(t_eval, k2):
    return euler_integrate(k2, t_eval)

if __name__ == "__main__":
    pass
    # TODO: Fit the model using curve_fit
    # popt, pcov = curve_fit(model_wrapper, time_data, conc_data, p0=[1.0])

    # TODO: Save plot to fit_plot.png

    # TODO: Write result to result.txt
EOF

    chmod -R 777 /home/user