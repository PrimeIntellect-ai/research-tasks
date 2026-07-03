You are acting as a bioinformatics systems analyst. We are studying the spatial diffusion of a newly synthesized signaling protein along a 1D biological tissue of length $L=1$.

We have an initial model based on the steady-state reaction-diffusion equation:
$$D \frac{d^2 C}{dx^2} - k C = 0$$
where $C(x)$ is the protein concentration, $D = 0.01$ is the diffusion coefficient, and $k = 0.1$ is the degradation rate. The boundary conditions are $C(0) = 1$ (source) and $C(1) = 0$ (sink).

Your task has two phases. You may use any programming language, but you must complete the setup, computation, and output formatting entirely within the terminal.

**Phase 1: Analytical Validation & Mesh Refinement**
1. The analytical solution to this equation is $C_{exact}(x) = \frac{\sinh(\sqrt{k/D}(1-x))}{\sinh(\sqrt{k/D})}$.
2. Write a numerical solver using standard second-order finite differences to solve the equation. 
3. Implement a mesh refinement loop: Start with $N=5$ grid points (including boundaries $x=0$ and $x=1$). Solve the system, then calculate the maximum absolute error between your numerical solution and the analytical solution at the grid points. If the maximum absolute error is $\ge 10^{-3}$, double the number of intervals (i.e., new $N = 2(N-1) + 1$), and repeat. 
4. Record the final $N$ required to achieve a maximum error $< 10^{-3}$, and the corresponding maximum error.

**Phase 2: Bootstrap Confidence Intervals on Noisy Data**
A sequencing pipeline has provided experimental measurements of this protein at four specific locations. The data is available at `/home/user/protein_counts.csv`. 
The CSV has four columns: `x_0.2`, `x_0.4`, `x_0.6`, `x_0.8`.
1. Read this CSV.
2. For each location, compute the 95% bootstrap confidence interval for the **mean** concentration. Use exactly 10,000 bootstrap resamples.
3. Use a random seed of `42` for your random number generator during bootstrapping to ensure reproducibility (if using Python, `numpy.random.seed(42)`). Calculate the lower and upper bounds using the 2.5th and 97.5th percentiles.

**Final Output**
Create a JSON file at `/home/user/analysis_report.json` exactly matching this structure:
```json
{
  "analytical_validation": {
    "final_N": <integer>,
    "max_error": <float>
  },
  "bootstrap_95_ci": {
    "x_0.2": [<lower_float>, <upper_float>],
    "x_0.4": [<lower_float>, <upper_float>],
    "x_0.6": [<lower_float>, <upper_float>],
    "x_0.8": [<lower_float>, <upper_float>]
  }
}
```

*Note: You may need to install necessary packages (like numpy/scipy) depending on your language choice.*