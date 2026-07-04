You are an AI assistant helping a bioinformatics researcher analyze observational data from a recent set of simulations. 

The researcher has a CSV file located at `/home/user/observational_data.csv` containing simulated biological sequences and their biochemical properties. The columns are `ID,Sequence,Binding_Affinity,Concentration`.

The researcher attempted to use a matrix factorization tool to find correlations, but it failed due to near-singular inputs caused by highly repetitive, malformed sequences in the dataset. To bypass this, you need to manually filter, reshape the data, and perform a linear regression using only standard Bash tools (like `awk`, `grep`, `sed`, etc. - no Python or R allowed).

Here are your instructions:
1. **Filter by Primer Design:** Only consider sequences that start with the exact motif `ATGC` and end with the exact motif `CGTA`.
2. **Filter by Concentration:** From the primer-filtered sequences, only keep the rows where `Concentration` is strictly greater than `10.0`.
3. **Calculate GC Content:** For these valid sequences, calculate the GC content (X). The GC content is the total number of 'G' and 'C' characters divided by the total length of the sequence.
4. **Curve Fitting / Regression:** Perform a simple ordinary least squares (OLS) linear regression to predict `Binding_Affinity` (Y) based on GC content (X). Calculate the slope and the y-intercept.
5. **Output Formatting:** Write the results to `/home/user/regression_results.txt` in exactly the following format (numerical values rounded to 4 decimal places):
```
Valid_Sequences: <count>
Slope: <slope_value>
Intercept: <intercept_value>
```

Make sure to strictly use Bash and standard POSIX command-line utilities. Do not write or execute any Python, Perl, R, or other high-level language scripts to solve the task.