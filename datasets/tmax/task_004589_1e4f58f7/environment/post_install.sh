apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy

    mkdir -p /home/user
    cat << 'EOF' > /home/user/generate_inputs.py
import numpy as np

# Generate 50 specific values for C
# We intentionally include values near C = 2.0 and C = -2.0 because
# the derivative 3x^2 - 3 is 0 at x = +/- 1.
# At x=1, f(1) = 1 - 3 - C = -2 - C => C = -2
# At x=-1, f(-1) = -1 + 3 - C = 2 - C => C = 2
# These points will cause instability.

c_values = np.linspace(-4.0, 4.0, 40).tolist()
c_values += [1.999, 2.000, 2.001, 2.002, 2.003] # Near instability
c_values += [-1.999, -2.000, -2.001, -2.002, -2.003]

with open('/home/user/inputs.txt', 'w') as f:
    for c in c_values:
        f.write(f"{c:.5f}\n")
EOF
    python3 /home/user/generate_inputs.py
    rm /home/user/generate_inputs.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user