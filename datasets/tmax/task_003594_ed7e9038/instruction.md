You are a bioinformatics analyst working on an RNA degradation study. We have a set of RNA sequences and need to simulate their decay over time in a cellular environment. 

We have received an image artefact from our wet-lab partners located at `/app/kinetics.png`. This image contains a scanned table of the kinetic degradation rate parameters ($k_{base}$, $k_A$, $k_U$, $k_G$, $k_C$).

You have a dataset of 5,000 RNA sequences located at `/home/user/rna_data.csv` (one sequence per line, starting on the second line as the first line is a header `Sequence`).

Your task is to write and execute a C++ program (`/home/user/simulate_decay.cpp`) that performs the following workflow:

1. **Parameter Extraction**: Extract the parameters from `/app/kinetics.png`. You may use the preinstalled `tesseract` OCR tool in the terminal to read the image, then use those values in your C++ code.
2. **Rate Calculation**: For each sequence, calculate its specific decay rate constant $k$:
   $k = k_{base} + \frac{count(A) \cdot k_A + count(U) \cdot k_U + count(G) \cdot k_G + count(C) \cdot k_C}{length\_of\_sequence}$
3. **ODE Simulation**: The concentration $C(t)$ of each RNA sequence follows this non-linear ordinary differential equation:
   $\frac{dC}{dt} = -k \cdot C - 0.002 \cdot C^2$
   Assume an initial concentration $C(0) = 100.0$. Use the 4th-order Runge-Kutta (RK4) method to numerically integrate this ODE from $t=0$ to $t=20$ with a time step of $\Delta t = 0.1$.
4. **Parallelization**: The ODE integration for the 5,000 sequences must be parallelized using OpenMP to ensure efficiency.
5. **Statistical Analysis**: After finding the final concentration $C(20)$ for all sequences, compute the 95% Bootstrap Confidence Interval for the **mean** final concentration of the population. Use 2,000 bootstrap iterations (sampling with replacement).
6. **Output**: Write the results to `/home/user/ci_results.csv` with exactly this format (comma-separated, one line of data with a header):
   ```
   Mean,Lower95,Upper95
   12.345,11.987,12.654
   ```

Requirements:
- Compile your C++ code with `-O3` and `-fopenmp`.
- Do not use root privileges. 
- You must output the file `/home/user/ci_results.csv` upon successful execution. Ensure your final values are accurate numerical estimates.