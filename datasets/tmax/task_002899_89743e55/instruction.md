You are an analyst in a bioinformatics lab. We are modeling the synthetic expression of several biological sequences. 

You have been provided with the following files in the `/app` directory:
1. `/app/sequences.fasta`: A FASTA file containing 100 synthetic nucleotide sequences.
2. `/app/simulate.py`: A Python script containing an adaptive step-size Euler integrator intended to simulate the protein concentration `P(t)` over time for a given sequence. The ODE is: `dP/dt = k_syn - k_deg * P`, where `P(0) = 0`.
3. `/app/lab_notes.png`: An image of a lab notebook snippet containing the experimentally determined degradation rate, `k_deg`.

Your tasks are:
1. **Extract Parameters:** Use OCR (e.g., `tesseract`, which is installed) to read `/app/lab_notes.png` and extract the numerical value for `k_deg`.
2. **Determine Synthesis Rates:** For each sequence in the FASTA file, calculate the GC content (the fraction of 'G' and 'C' bases out of the total sequence length). The synthesis rate for each sequence is defined as `k_syn = 5.0 * GC_fraction`.
3. **Debug the Simulator:** The provided numerical integrator in `/app/simulate.py` diverges or produces `NaN` because the step-size adaptation logic is fundamentally flawed (it increases the step size when the local error is high, rather than decreasing it). Fix the step-size adaptation bug in `simulate.py` so that it accurately integrates the ODE up to `t_end = 100`.
4. **Simulate:** Run your corrected integrator for all 100 sequences to find the final steady-state concentration `P(100)` for each sequence.
5. **Distribution Fitting:** Assuming the 100 final concentration values are drawn from a Normal distribution `N(mu, sigma^2)`, calculate the Maximum Likelihood Estimates for the mean (`mu`) and standard deviation (`sigma`) of these steady states.
6. **Output:** Create a JSON file at `/app/results.json` with the following exact structure:
```json
{
  "k_deg": 0.0,
  "mu": 0.0,
  "sigma": 0.0,
  "concentrations": {
    "seq_1": 0.0,
    "seq_2": 0.0,
    ...
  }
}
```
Replace the `0.0` values with your computed results (use the sequence IDs from the FASTA file as keys in the `concentrations` dictionary).

Your work will be graded programmatically based on the accuracy of your final computed concentrations compared to the true analytical solutions of the ODE.