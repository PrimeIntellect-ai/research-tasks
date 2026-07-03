You are a researcher conducting a computational experiment to simulate the radioactive decay of a two-step isotope chain and the resulting gamma-ray spectrum measured by a detector.

Your task is to write and run a Rust program that performs this simulation.

### Instructions:

1. **Environment Setup:**
   - Create a new Rust Cargo project at `/home/user/decay_sim`.
   - You may use the following crates: `rand` (v0.8), `rand_chacha` (v0.3), and `rand_distr` (v0.4).

2. **ODE Numerical Solving:**
   - Isotope A decays into Isotope B, which then decays into a stable isotope.
   - Initial populations: $A = 1,000,000.0$, $B = 0.0$.
   - Decay constants: $\lambda_A = 0.1 \text{ s}^{-1}$, $\lambda_B = 0.05 \text{ s}^{-1}$.
   - Simulate from $t=0$ to $t=60$ seconds using Euler's method with a time step of $\Delta t = 1.0 \text{ s}$.
   - For each step (representing the interval from $t$ to $t+1$):
     - `decay_A = \lambda_A * A * \Delta t`
     - `decay_B = \lambda_B * B * \Delta t`
     - Update populations: 
       - $A_{new} = A - \text{decay\_A}$
       - $B_{new} = B + \text{decay\_A} - \text{decay\_B}$
     - Keep $A$ and $B$ as floating-point numbers. Do not round them.

3. **Monte Carlo Simulation & Spectroscopy:**
   - Each decay of Isotope B emits a photon. The detector only captures a fraction of these photons.
   - For each 1-second interval, the number of photons detected is `floor(decay_B * 0.1)`. Calculate this as an integer.
   - For each detected photon, simulate its measured energy by sampling from a Normal distribution with $\text{mean} = 500.0 \text{ keV}$ and $\text{standard deviation} = 20.0 \text{ keV}$.
   - **Crucial:** To ensure reproducibility, initialize a `ChaCha8Rng` pseudo-random number generator with the seed `42` at the very beginning of your program. Draw the random energies using this exact RNG and `rand_distr::Normal`.

4. **Data Processing:**
   - Bin the detected photon energies into a histogram spanning from 400.0 keV to 600.0 keV with a bin width of 5.0 keV. 
   - The first bin is `[400.0, 405.0)`, the second is `[405.0, 410.0)`, and so on, up to `[595.0, 600.0)`.
   - Ignore any photons with energies outside the `[400.0, 600.0)` range.
   
5. **Output:**
   - Write the resulting histogram to a CSV file at `/home/user/spectrum.csv`.
   - The file must contain exactly 40 lines. Each line must be formatted as `bin_start,count`.
   - Example lines:
     ```
     400,12
     405,27
     ```

Write the code, compile it, and run it to produce `/home/user/spectrum.csv`.