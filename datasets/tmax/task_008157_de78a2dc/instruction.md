You are a Machine Learning Engineer preparing genomic training data. Your data processing pipeline (analogous to a numerical integrator) diverges and fails when the statistical distribution of a localized region shifts too dramatically from the global distribution.

Your task is to implement a Bash-only solution (using standard CLI tools like `awk`, `sed`, `grep`, `bash`, etc. without Python or Perl) to decompose a genomic sequence into meshes (windows) and detect these anomalous regions.

The input file is located at `/home/user/genome.fasta`. 

Write a script and/or use terminal commands to do the following:
1. Parse the FASTA file to extract the full combined DNA sequence (ignore header lines starting with `>`).
2. Calculate the "global GC-ratio": the fraction of 'G' and 'C' characters over the entire sequence length.
3. Perform a domain decomposition by splitting the sequence into non-overlapping windows (chunks) of exactly 50 bases. Discard any trailing bases that do not form a complete 50-base window.
4. For each 50-base chunk, calculate its local GC-ratio.
5. Calculate the distance metric: the absolute difference between the local GC-ratio and the global GC-ratio.
6. Identify the chunks where this distance is strictly greater than `0.2000`.

Output the anomalous chunks to a tab-separated log file at `/home/user/outliers.tsv`.
The file must have the following format for each anomalous chunk:
`[ChunkIndex]    [ChunkSequence]    [Distance]`

Where:
- `[ChunkIndex]` is the 1-based index of the 50-base window (e.g., the first 50 bases is index 1).
- `[ChunkSequence]` is the exact 50-base string.
- `[Distance]` is the absolute difference rounded to exactly 4 decimal places (e.g., `0.3000`).

Ensure your final output file strictly adheres to this format.