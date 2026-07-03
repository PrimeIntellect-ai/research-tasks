You are a data scientist tasked with fitting a biochemical model. Your pipeline has been producing non-reproducible and inaccurate results due to floating-point reduction order issues when accumulating millions of small simulation residuals, which subsequently destabilizes your nonlinear root-finding step.

You must fix the pipeline by calculating the exact sum of the residuals using a numerically stable algorithm, use that sum to solve a nonlinear equation dependent on protein sequence data, and rigorously log the convergence.

**Step 1: Parse Biological Data**
There is a protein sequence file at `/home/user/kinetics/sequence.fasta`.
Parse this file to determine the exact number of amino acids (sequence length, `L`). Ignore whitespace and header lines.

**Step 2: Stable Summation**
There is a large text file at `/home/user/kinetics/sim_data.txt` containing one floating-point number per line. 
If you sum these directly using standard accumulation (especially in 32-bit floats), precision is lost due to the combination of vastly different magnitudes. 
Implement the **Kahan summation algorithm** (compensated summation) in the language of your choice to sum all values in `sim_data.txt`. Let this precise sum be `S`.

**Step 3: Nonlinear Equation Solving and Convergence Testing**
The core physical model requires finding the real root `x` of the following nonlinear equation:
`x^3 + L * x - S = 0`

You must implement a custom **Newton-Raphson solver** from scratch (do not use library root-finders like `scipy.optimize`) to find the root `x`.
* Start with an initial guess of `x_0 = 1.0`.
* Iterate until the absolute difference between successive guesses $|x_{n} - x_{n-1}|$ is less than `1e-7`.
* Log the absolute difference at *each step* to `/home/user/kinetics/convergence.txt` (one number per line, starting from the difference between `x_1` and `x_0`).

**Step 4: Output Verification**
Write your final values to a JSON file at `/home/user/kinetics/solution.json` with exactly these keys:
- `"L"`: The sequence length (integer).
- `"kahan_sum"`: The Kahan sum `S` (float, rounded to 4 decimal places).
- `"root"`: The final converged root `x` (float, rounded to 6 decimal places).

Create your scripts and run them to generate the required output files.