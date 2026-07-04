You are a bioinformatics analyst tasked with modeling a reaction-diffusion network dependent on sequence-specific binding affinities. 

Your task has three main parts:

1. **Fix and Install a Vendored Package**
We have a proprietary Python C-extension called `seq_affinity` located at `/app/seq_affinity-0.2.1`. It calculates binding affinities from DNA sequences. However, the package currently fails to build because its `setup.py` is missing the required OpenMP compiler flags (it relies on OpenMP pragmas internally). 
Fix the `setup.py` file to include the appropriate flags (e.g., `-fopenmp` for GCC) in both `extra_compile_args` and `extra_link_args`, then install the package in the current Python environment.

2. **Develop the Analysis Script**
Create a script at `/home/user/analyze.py` that takes a single command-line argument: the path to a text file containing DNA sequences (one sequence per line).

For each sequence in the file:
a. Calculate its binding affinity $k$ using `seq_affinity.calculate_k(sequence)`.
b. Use this $k$ to solve the following nonlinear ODE system from $t = 0$ to $t = 10$:
   $$ \frac{dA}{dt} = k \cdot B - 0.1 \cdot A^2 $$
   $$ \frac{dB}{dt} = -k \cdot B + 0.1 \cdot A $$
   Initial conditions: $A(0) = 0.0$, $B(0) = 1.0$.
   Use `scipy.integrate.solve_ivp` with the default RK45 solver and `rtol=1e-6`, `atol=1e-8`.
   Extract the value of $A$ at exactly $t = 10$. Let's call this $A_{10}$.

3. **Bootstrap Confidence Intervals**
After computing $A_{10}$ for all sequences in the input file, calculate the 95% bootstrap confidence interval for the **mean** of $A_{10}$.
- You MUST set the random seed exactly via `numpy.random.seed(42)` immediately before running the bootstrap loop.
- Perform exactly $N=10,000$ resamples (with replacement) of your $A_{10}$ array.
- For each resample, compute the mean.
- Find the 2.5th and 97.5th percentiles of these 10,000 means using `numpy.percentile` (using the default 'linear' interpolation method).

Your script must print exactly one line to standard output in this exact comma-separated format:
`Mean,CI_lower,CI_upper`
Where all three values are rounded to exactly 4 decimal places.

Example output:
`0.4521,0.4310,0.4732`