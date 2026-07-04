You are a bioinformatics researcher working on a simulation of targeted PCR amplification. 

You have been provided with a Python script `/home/user/pcr_model.py` that models DNA amplification using a logistic growth differential equation: 
`dY/dt = r * Y * (1 - Y/K)`, with an initial concentration `Y(0) = 2.0`.

Currently, the numerical integrator inside `pcr_model.py` is failing its basic regression tests because the forward Euler step-size (`dt`) is set too large, causing the simulation to oscillate and diverge. 

Your tasks are:
1. **Fix the Integration & Regression Test**: Modify `/home/user/pcr_model.py` so that the integration is stable and accurate (you may reduce the step size or switch to a robust solver like `scipy.integrate.solve_ivp`). The script includes a test function that compares your simulation output against an expected analytic curve. When fixed, running `python /home/user/pcr_model.py --test` should print "Test passed!" and exit with code 0.
2. **Curve Fitting**: A real-world dataset is located at `/home/user/reference_yield.csv` (containing columns `time` and `yield`). Write code to fit the logistic growth model to this data to estimate the true amplification rate `r` and carrying capacity `K`.
3. **Primer Selection**: The amplification rate `r` correlates with the optimal primer length `L` required for this specific variant, defined by the formula `L = int(r * 20)`. You have a set of candidate primers in `/home/user/candidates.fasta` and a reference target gene sequence in `/home/user/gene_sequence.txt`. Find the primer from the FASTA file that is exactly `L` nucleotides long AND perfectly aligns (is an exact substring match) to the sequence in `gene_sequence.txt`.
4. **Output Generation**: Create a file named `/home/user/solution.json` containing the fitted parameters (rounded to 2 decimal places) and the matching primer ID. 

The JSON must exactly match this structure:
```json
{
  "fitted_r": 0.00,
  "fitted_K": 0.00,
  "primer_id": "primer_name"
}
```

Ensure all dependencies (e.g., `scipy`, `pandas`, `numpy`) are installed or install them via pip if necessary.