You are a researcher working on a radiation shielding simulation. You have been given raw observational data from a series of detector tests and need to estimate the material's attenuation coefficient, run a Monte Carlo simulation to validate the behavior at a new thickness, and compare the simulation to the analytical solution.

Your tasks are:

1. **Observational Data Reshaping**:
   You have a file at `/home/user/sensor_data.txt`. Each line contains a pipe-delimited record: `sensor_name|thickness_mm|count`.
   There are multiple sensor readings for each thickness. Write a Rust script to read this file, parse the data, and calculate the average `count` for each `thickness_mm`.

2. **Nonlinear Equation Solving (Parameter Estimation)**:
   The physical model for the average count $C(x)$ at thickness $x$ (in mm) is given by:
   $$C(x) = C_0 e^{-\mu x} + B$$
   Where:
   * $C_0 = 100,000$ (initial particle intensity)
   * $B = 200$ (background radiation count)
   * $\mu$ is the unknown attenuation coefficient (in mm$^{-1}$).
   
   Using the averaged data from step 1, solve for $\mu$. (The data is generated such that $\mu$ is constant; you can use any data point $x > 0$ to find $\mu$).

3. **Monte Carlo Simulation**:
   Write a Rust program to simulate the transmission of particles through a shield of thickness $x = 15.0$ mm.
   * Simulate $N = 1,000,000$ independent particles.
   * For each particle, its penetration depth $d$ before interacting is exponentially distributed: $d = -\frac{\ln(R)}{\mu}$, where $R$ is a uniform random number in $(0, 1]$.
   * A particle is "transmitted" if $d > 15.0$.
   * Count the total number of transmitted particles.

4. **Analytical Validation**:
   Calculate the analytical transmission probability for a single particle through $15.0$ mm, which is $P = e^{-15 \mu}$.

5. **Output**:
   Generate a JSON log file at `/home/user/final_analysis.json` with exactly the following keys:
   * `"mu_estimated"`: The calculated $\mu$ as a float, rounded to 3 decimal places.
   * `"analytical_prob"`: The theoretical transmission probability at 15.0 mm as a float, rounded to 4 decimal places.
   * `"mc_transmitted_count"`: The integer number of particles transmitted in your Monte Carlo simulation (out of 1,000,000).

You may use `cargo` to create any Rust projects and include dependencies like `rand` or `serde_json` as needed. Run your code to produce the final JSON file.