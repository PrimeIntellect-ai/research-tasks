You are tasked with fixing and upgrading a distributed simulation pipeline for a computational physics lab. The lab is simulating heat diffusion with a time-varying boundary source, and we need to analyze the frequency spectrum of the thermal response at a specific sensor location. 

The pipeline consists of three services:
1. **Redis**: Used as a message broker and cache.
2. **Flask API Server**: Distributes simulation parameters and collects results.
3. **Simulation Worker**: Fetches parameters, runs the PDE simulation, performs signal processing (spectroscopy/FFT) on the output, and submits the result.

Currently, the pipeline is broken and the numerical solver is inaccurate. Your goals are:

**1. Fix the Multi-Service Architecture:**
The startup script `/app/start.sh` launches Redis (port 6379) and the Flask server (port 5000). The worker script `/app/worker.py` is failing to connect to the Flask API to get jobs. You need to fix `/app/worker.py` so it properly queries `http://127.0.0.1:5000/job`, which returns JSON: `{"alpha": 0.05, "duration": 10.0, "dt": 0.01}`.

**2. Implement the PDE Solver with Mesh Refinement:**
The worker must simulate the 1D Heat Equation:
$u_t = \alpha u_{xx}$
on the domain $x \in [0, 1]$ for $t \in [0, duration]$.
Boundary conditions:
- $u(0, t) = \sin(15 t) + 0.5 \sin(40 t)$
- $u(1, t) = 0$
Initial condition: $u(x, 0) = 0$.

The current implementation in `/app/worker.py` uses an explicit Euler scheme with only 5 spatial grid points, which is unstable and wildly inaccurate. You must replace this with a stable numerical solver (e.g., implicit method, Crank-Nicolson, or Method of Lines using `scipy.integrate.solve_ivp`). You must use a refined spatial mesh of exactly $N_x = 101$ points (so $dx = 0.01$). Evaluate the solution at time steps $dt = 0.01$ (i.e., 1001 time points from 0.0 to 10.0 inclusive).

**3. Signal Processing:**
Extract the temperature time-series at the sensor location $x = 0.5$.
Compute the discrete Fourier transform (FFT) of this time-series $u(0.5, t)$ to obtain the amplitude spectrum.
You must compute the absolute value of the FFT (amplitudes) and normalize it by dividing by the number of time points (1001).
Keep only the positive frequencies (from index 0 up to and including the Nyquist frequency limit, i.e., the first 501 points).

**4. Submission:**
Modify `/app/worker.py` to post the final array of 501 amplitude values as a JSON list to `http://127.0.0.1:5000/submit`.
The Flask server will save this to `/home/user/result_spectrum.json`.

**Success Criteria:**
We will compute the Mean Squared Error (MSE) between your submitted amplitude spectrum and a high-resolution reference spectrum. Your MSE must be strictly less than `1e-4`.

You can start the backend services by running:
`bash /app/start.sh &`
Then write/fix the worker script and run it. Do not modify the Flask server code.