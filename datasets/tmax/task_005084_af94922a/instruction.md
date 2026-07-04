You are a bioinformatics data scientist tasked with analyzing a set of candidate PCR primers. You need to identify which primers uniquely target a reference genome and then determine their melting temperatures ($T_m$) from experimental fluorescence data.

Your task is to write and execute a Python script (`/home/user/analyze_primers.py`) that performs the following steps:

1. **Sequence Alignment (Exact Match):** 
   Read `/home/user/reference.fasta` and `/home/user/primers.fasta`. 
   Find all primers that have *exactly one* perfect match in the reference genome. You must check both the forward sequence and the reverse complement of the primer. Primers with 0 matches or >1 matches (summing both forward and reverse complement occurrences) must be discarded.

2. **Curve Fitting:**
   For the valid, unique primers identified in step 1, analyze their thermal melting curves using the data in `/home/user/melting_data.csv`. The CSV has three columns: `primer_id`, `temperature`, and `fluorescence`.
   Fit the data for each valid primer to the following logistic function to find the melting temperature $T_m$:
   $$F(T) = \frac{L}{1 + e^{-k(T - T_m)}} + b$$
   Where:
   - $T$ is the temperature.
   - $F(T)$ is the fluorescence.
   - $L, k, T_m, b$ are parameters to be fitted.
   - $T_m$ is the melting temperature (inflection point).
   *Hint: `scipy.optimize.curve_fit` is highly recommended.*

3. **Parallel Computing:**
   Because curve fitting over thousands of primers can be slow, you must implement the curve fitting step in parallel using Python's `multiprocessing` module (e.g., `multiprocessing.Pool`).

4. **Output:**
   Save the final results to `/home/user/valid_primers_tm.csv`. 
   The CSV must contain exactly two columns: `primer_id` and `Tm`.
   The `Tm` values must be rounded to exactly 2 decimal places.
   The rows must be sorted alphabetically by `primer_id`.

Ensure you run your script and that the final output file is generated successfully.