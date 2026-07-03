You are an ML engineer preparing a training dataset for a model that predicts DNA primer efficiency. You need to build a reproducible pipeline that extracts viable primers, calculates their sequence features, and computes a specific non-linear "stability index".

You have been given two files:
1. `/home/user/reference.fasta`: A standard FASTA file containing a single reference genome sequence.
2. `/home/user/candidates.txt`: A text file containing candidate primer sequences (one per line).

Your task is to create a Python script (`/home/user/prepare_data.py`) and a Bash pipeline script (`/home/user/run_pipeline.sh`) to perform the following steps:

1. **Alignment / Filtering**: Read `candidates.txt` and keep only the sequences that are exact substrings of the DNA sequence in `reference.fasta` (ignoring the `>...` header line and any newlines in the sequence).
2. **Feature Extraction**: For each valid primer, calculate:
    - $L$: The length of the sequence.
    - $GC$: The GC-content (the fraction of letters that are 'G' or 'C', as a float between 0.0 and 1.0).
3. **Non-linear Equation Solving**: For each valid primer, calculate the stability index $x$. The stability index is defined as the root of the following non-linear equation:
   $$e^{x/L} + x \cdot \ln(GC + 0.1) - 10 = 0$$
   Use a standard numerical solver (like `scipy.optimize.fsolve`) with an initial guess of $x = 1.0$.
4. **Output**: The Python script should output a CSV file at `/home/user/training_data.csv` with the exact header `sequence,L,GC,x`. 
   - $GC$ and $x$ must be rounded to exactly 4 decimal places.
   - The rows should be written in the order the valid sequences appeared in `candidates.txt`.

Finally, ensure that running `bash /home/user/run_pipeline.sh` executes your Python script and generates the `training_data.csv` successfully. 

Requirements:
- Ensure your Python script handles the math properly (use `math` and `scipy.optimize`).
- Do not use any external alignment tools like BLAST; simple string matching in Python is required for this dataset.
- The pipeline script must be executable.