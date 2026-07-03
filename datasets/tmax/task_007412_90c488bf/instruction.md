You are a bioinformatics analyst working on a dynamic model of gene expression. We are modeling the mRNA concentration $M(t)$ over time for several genes. 

The dynamics of mRNA concentration follow the differential equation:
$dM/dt = \alpha - \gamma M$
where $\alpha$ is the transcription rate and $\gamma$ is the decay rate. The initial condition is $M(0) = 0$.

We derive $\alpha$ and $\gamma$ directly from the gene sequence:
- $\alpha = 1000 / L$, where $L$ is the sequence length.
- $\gamma = 0.05 + 2.0 \times |GC - 0.5|$, where $GC$ is the GC-content fraction of the sequence (number of G and C bases divided by $L$).

You have been provided a FASTA file at `/home/user/genes.fasta`.

Your task is to write a Python script `/home/user/run_model_test.py` that performs regression testing on a numerical solver by comparing it against the analytical solution. The script must do the following for each sequence in the FASTA file:

1. Calculate $L$, $GC$, $\alpha$, and $\gamma$.
2. Compute the exact analytical solution for mRNA concentration at time $t=50$. The analytical solution is $M(t) = (\alpha/\gamma) \times (1 - e^{-\gamma t})$.
3. Perform numerical integration to find $M(50)$ using the standard Euler method. Use a time step of $\Delta t = 0.1$ from $t=0$ to $t=50$ (exactly 500 steps, where the final value is at $t=50$).
4. Compute the numerical derivative $dM/dt$ at $t=50$ using the backward difference from your numerical integration results: $(M(50) - M(49.9)) / \Delta t$.
5. Determine if the numerical integration passes the regression test. It passes (`True`) if the absolute difference between the analytical $M(50)$ and numerical $M(50)$ is strictly less than $1.0$. Otherwise, `False`.

Save your results to `/home/user/regression_report.json`. The output must be a JSON array of objects, one for each sequence (in the same order as the FASTA file), with exactly these keys:
- `"seq_id"`: The sequence ID (e.g., "seq1").
- `"analytical_M50"`: Float, the analytical solution at t=50.
- `"numerical_M50"`: Float, the Euler method solution at t=50.
- `"numerical_derivative_M50"`: Float, the backward difference derivative at t=50.
- `"passed_regression"`: Boolean, as defined in step 5.

Run your script to generate the JSON file.