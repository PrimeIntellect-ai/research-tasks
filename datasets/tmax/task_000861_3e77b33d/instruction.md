You are acting as a research assistant in a computational physics lab. We are running Monte Carlo simulations of a stochastic damped harmonic oscillator, representing a trapped nanoparticle subjected to thermal noise. 

Our core simulation engine is a legacy, stripped compiled executable located at `/app/bin/sim_engine`. This binary solves the Langevin equations using a naive Euler-Maruyama integration scheme. It takes arguments like `--steps 1000 --dt 0.01 --out trajectory.csv` and outputs a CSV file with columns `time,x`.

**The Problem:**
Because the binary uses an explicit ODE solver, the numerical integration occasionally becomes unstable for certain random noise realizations. When this happens, the trajectory exhibits unphysical numerical blow-up. We have collected a dataset of known "clean" (physically valid) and "evil" (numerically unstable) trajectories. 

**Your Task:**
Write a Python script `/home/user/filter.py` that acts as an automated regression filter. It must take a single command-line argument (the path to a CSV file) and determine if the trajectory is physically valid or if it suffered from numerical instability.

1. **Calculate Velocity:** The CSV only contains time `t` and position `x`. You must compute the velocity $v(t)$ using second-order accurate central finite differences (use forward/backward differences for the endpoints).
2. **Calculate Energy:** Compute the total mechanical energy at each time step: $E(t) = \frac{1}{2} m v(t)^2 + \frac{1}{2} k x(t)^2$. The system parameters are mass $m = 1.0$ and spring constant $k = 5.0$.
3. **Classification Rules:** 
   - A trajectory is unstable ("evil") if its total energy $E(t)$ exceeds `50.0` at any point, OR if the absolute energy jump between any two consecutive time steps $|\Delta E|$ is greater than `10.0`.
   - Otherwise, the trajectory is "clean".
4. **Output:** 
   - If the trajectory is CLEAN, the script must exit with status code `0`.
   - If the trajectory is EVIL (unstable), the script must exit with status code `1`.

**Validation Corpora:**
You can test your script against our existing classification datasets:
- `/app/data/clean/` contains 100 verified stable trajectories.
- `/app/data/evil/` contains 100 verified unstable trajectories.

Ensure your script handles standard CSV parsing properly and strictly follows the exit code requirements.