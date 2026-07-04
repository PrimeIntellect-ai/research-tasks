You are a bioinformatics analyst tasked with finding high-complexity 15-bp primer sequences that are distinctly present in a target DNA sequence but stand out structurally from a background reference dataset.

You have been provided a JSON file at `/home/user/sequences.json` containing two DNA sequences: `"target"` and `"background"`.

Your task is to write and execute a Python script that performs the following steps:

1. **Domain Decomposition**: Extract every possible contiguous 15-bp sequence window (rolling window, step size 1) from both the target and background sequences.
2. **Matrix Encoding**: Convert each 15-bp window into a 15x4 one-hot encoded matrix. The rows represent the 15 positions in the sequence. The 4 columns correspond to the nucleotides in alphabetical order: `A`, `C`, `G`, `T` (e.g., `A` is `[1, 0, 0, 0]`, `C` is `[0, 1, 0, 0]`, etc.).
3. **Matrix Decomposition**: For each encoded window matrix $M$, compute its Singular Value Decomposition (SVD). Calculate its "complexity score" defined as the *nuclear norm* (the sum of its singular values).
4. **Reference Dataset Comparison**: Find the maximum complexity score among all 15-bp windows derived from the `"background"` sequence. Let this value be $B_{max}$.
5. **Filtering**: Identify all 15-bp windows from the `"target"` sequence that have a complexity score *strictly greater* than $B_{max}$.
6. **Output**: Save the unique, valid 15-bp candidate target sequences to `/home/user/candidates.txt`. The sequences must be written one per line, sorted alphabetically.

The `/home/user/sequences.json` file has the following format:
```json
{
  "target": "ATGCACGTGACTAGCTACGATCGATCGTACGATCGATCGATCG",
  "background": "ATATATATATGCGCATATATATATATATATATATATATATATA"
}
```

Ensure your script runs successfully and creates the `/home/user/candidates.txt` file exactly as specified.