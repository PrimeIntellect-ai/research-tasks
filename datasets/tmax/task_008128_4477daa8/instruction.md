You are a performance engineer tasked with profiling and optimizing a Monte Carlo simulation. 

A data scientist has provided a Jupyter Notebook located at `/home/user/simulation.ipynb`. This notebook contains a prototype of a stochastic differential equation (SDE) simulation using the Euler-Maruyama method. The simulation tracks 10,000 independent particles over time. 

Currently, the simulation has two major issues:
1. **Performance:** It uses a slow, nested Python `for` loop to iterate over both time steps and individual particles.
2. **Numerical Instability:** The numerical integrator diverges for certain step sizes (`dt`), causing values to explode to infinity or `NaN` because of improper step-size adaptation in the cubic drift term.

Your task is to fix these issues by vectorizing the simulation and profiling it to find the optimal step size. 

Perform the following steps:
1. Extract the Python code from the notebook `/home/user/simulation.ipynb`.
2. Rewrite the simulation logic into a pure Python script that uses multi-dimensional array manipulation (NumPy) to completely eliminate the loop over particles. All 10,000 particles must be updated simultaneously in a single vectorized operation inside the time loop.
3. Profile the simulation's stability by testing the following step sizes (`dt`) in order: `0.1`, `0.05`, `0.025`, `0.01`, `0.005`, `0.001`.
4. For each `dt`, the simulation must run from `t = 0.0` to `t = 2.0`. 
5. A simulation run is considered "diverged" if the absolute value of any particle exceeds `1000.0`, or if any value becomes `NaN` or `infinity` at the end of the simulation.
6. Find the **largest** `dt` from the list above that does **not** diverge.

**Simulation Specifications to ensure perfect reproducibility:**
*   **Equation:** $X_{t+dt} = X_t + (-X_t^3 + 2X_t)dt + \sqrt{dt} Z_t$
*   **Particles:** $N = 10000$
*   **Total Time:** $T = 2.0$. The number of steps is exactly `int(2.0 / dt)`.
*   **Random Initialization:** Before running the simulation for a specific `dt`, you must call `np.random.seed(42)`. Then, initialize $X_0 \sim N(0, 1)$ for all 10,000 particles using `np.random.randn(10000)`.
*   **Stochastic Term:** At each time step, generate the noise $Z_t \sim N(0, 1)$ for all particles using `np.random.randn(10000)`. 

**Deliverables:**
1. Save your heavily optimized, vectorized Python code to `/home/user/vectorized_sim.py`.
2. Create a report file at `/home/user/report.txt`. 
   - The first line must contain the optimal (largest stable) `dt` you found.
   - The second line must contain the mean of the final values of all particles for that optimal `dt`, rounded to exactly 4 decimal places.