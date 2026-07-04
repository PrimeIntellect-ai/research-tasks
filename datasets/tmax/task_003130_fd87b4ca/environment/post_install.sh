apt-get update && apt-get install -y python3 python3-pip gcc build-essential
    pip3 install pytest numpy scipy

    mkdir -p /app
    mkdir -p /home/user/pipeline/data
    mkdir -p /home/user/pipeline/results

    # Hidden python reactor
    cat << 'EOF' > /app/.hidden_reactor.py
import sys
import numpy as np
from scipy.integrate import solve_ivp

if len(sys.argv) != 4:
    sys.exit(1)

try:
    k1, k2, k3 = map(float, sys.argv[1:4])
except:
    sys.exit(1)

def robertson(t, y):
    A, B, C = y
    dA = -k1 * A + k2 * B * C
    dB = k1 * A - k2 * B * C - k3 * B**2
    dC = k3 * B**2
    return [dA, dB, dC]

t_eval = np.linspace(0, 100, 100)
sol = solve_ivp(robertson, [0, 100], [1.0, 0.0, 0.0], method='BDF', t_eval=t_eval)

for i in range(len(sol.t)):
    print(f"{sol.t[i]} {sol.y[0][i]} {sol.y[1][i]} {sol.y[2][i]}")
EOF

    # C Wrapper for the blackbox reactor
    cat << 'EOF' > /app/reactor.c
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "python3 /app/.hidden_reactor.py %s %s %s", argv[1], argv[2], argv[3]);
    return system(cmd);
}
EOF
    gcc -o /app/blackbox_reactor /app/reactor.c
    strip /app/blackbox_reactor
    rm /app/reactor.c

    # Generate raw experiment data
    cat << 'EOF' > /tmp/gen_data.py
import numpy as np
from scipy.integrate import solve_ivp

k1, k2, k3 = 0.04, 10000, 30000000

def robertson(t, y):
    A, B, C = y
    dA = -k1 * A + k2 * B * C
    dB = k1 * A - k2 * B * C - k3 * B**2
    dC = k3 * B**2
    return [dA, dB, dC]

t_eval = np.linspace(0, 100, 100)
sol = solve_ivp(robertson, [0, 100], [1.0, 0.0, 0.0], method='BDF', t_eval=t_eval)

np.random.seed(42)
with open('/home/user/pipeline/data/raw_experiment.dat', 'w') as f:
    f.write("# This is a noisy experimental data file\n")
    f.write("# Format: time | A | B | C\n")
    for i in range(len(sol.t)):
        noise = np.random.normal(0, 0.05, 3)
        A = sol.y[0][i] + noise[0]
        B = sol.y[1][i] + noise[1]
        C = sol.y[2][i] + noise[2]
        if i % 10 == 0:
            f.write("   # some random comment\n")
        f.write(f"  {sol.t[i]} | {A} | {B} | {C} \n")
EOF
    python3 /tmp/gen_data.py
    rm /tmp/gen_data.py

    # Broken integrate.py
    cat << 'EOF' > /home/user/pipeline/integrate.py
import numpy as np

def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h/2, y + h/2 * k1)
    k3 = f(t + h/2, y + h/2 * k2)
    k4 = f(t + h, y + h * k3)
    return y + h/6 * (k1 + 2*k2 + 2*k3 + k4)

def integrate(k1, k2, k3):
    def f(t, y):
        A, B, C = y
        return np.array([
            -k1 * A + k2 * B * C,
            k1 * A - k2 * B * C - k3 * B**2,
            k3 * B**2
        ])

    t = 0
    y = np.array([1.0, 0.0, 0.0])
    h = 0.1

    times = [t]
    ys = [y]

    while t < 100:
        y = rk4_step(f, t, y, h)
        t += h
        times.append(t)
        ys.append(y)

    return np.array(times), np.array(ys)

if __name__ == "__main__":
    t, y = integrate(0.04, 10000, 30000000)
    print(y[-1])
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app