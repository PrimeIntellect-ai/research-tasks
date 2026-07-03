You are a bioinformatics analyst reviewing the output of a genomic sequence simulator. The simulation tracks the expected GC-skew (`sim_val`) across positional windows, but you suspect the underlying numerical integrator has diverged from the experimental data (`exp_val`) due to poor step-size adaptation.

You have been provided with a dataset at `/home/user/sequence_signal.csv`. It contains three columns: `pos`, `exp_val`, and `sim_val`. The first row is the header.

Using **only standard shell utilities** (e.g., `awk`, `bash`, `sed`, `grep`, `bc`, `jq`), analyze this file and compute the following metrics:
1. **Max Derivative**: Calculate the discrete derivative $\frac{d(exp\_val)}{d(pos)}$ between consecutive points (i.e., $\frac{exp\_val_{i} - exp\_val_{i-1}}{pos_{i} - pos_{i-1}}$). Find the maximum absolute value of this derivative across the entire dataset.
2. **Divergence Position**: The simulated sequence diverged. Find the *first* `pos` where the absolute difference between `exp_val` and `sim_val` is strictly greater than `50.0`.
3. **Initial Slope**: Perform a least-squares linear regression to find the slope of `exp_val` as a function of `pos`, using **only the first 10 data rows** (ignoring the header). 

Create a report file at `/home/user/analysis_report.txt` with exactly the following format. Round the `Max_Derivative` and `Initial_Slope` to exactly 2 decimal places. `Divergence_Pos` should be an integer.

```text
Max_Derivative: <value>
Divergence_Pos: <value>
Initial_Slope: <value>
```

Do not use Python, R, or any external scripting languages to compute the result; you must rely on standard Linux CLI tools.