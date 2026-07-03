You are a bioinformatics analyst tasked with analyzing dinucleotide transitions in DNA sequences. 

Your goals are to fix a broken bioinformatics package, use it to parse FASTA files, and implement a script that matches the exact output of a legacy oracle program.

Step 1: Fix the Vendored Package
We rely on a local package called `fastakit` to parse FASTA files, but the source code has been corrupted. 
1. Navigate to `/app/vendored/fastakit-0.1.0`.
2. Find and fix the deliberate parsing bug in `fastakit/reader.py`. The bug currently corrupts sequence data by incorrectly stripping characters from lines instead of standard whitespace/newlines.
3. Install the fixed package into your Python environment.

Step 2: Implement the Analysis Script
Write a Python script at `/home/user/analyze.py` that takes exactly one argument (the path to a FASTA file).
Your script must:
1. Use `fastakit.read_fasta(filepath)` to parse the file. Assume the file contains exactly one sequence.
2. Construct a 4x4 multi-dimensional array (matrix) of dinucleotide counts. The nucleotides must be ordered A, C, G, T. Rows represent the first nucleotide and columns represent the second. Overlapping dinucleotides should be counted (e.g., "GAAAT" has dinucleotides GA, AA, AA, AT).
3. Compute a simple Chi-square statistic comparing the observed dinucleotide counts to the expected counts under a null model of independent nucleotides. 
   - Expected count for dinucleotide XY = `(Count_X * Count_Y) / (L - 1)`
   - Where `Count_X` is the total count of nucleotide X in the sequence, `Count_Y` is the total count of nucleotide Y, and `L` is the total sequence length.
   - Chi-square = Sum over all 16 dinucleotides of `((Observed - Expected)^2 / Expected)`. If `Expected` is 0, add 0 to the sum for that term.
4. Output the results to standard output EXACTLY in the following format:
   ```
   [ID] <sequence_id>
   [MATRIX] <16 comma-separated integers, row-major order>
   [CHI2] <chi2_statistic_rounded_to_4_decimal_places>
   ```

Step 3: Verification Against the Oracle
A compiled reference oracle is located at `/opt/oracle/dinuc_oracle`. Your script's standard output must be bit-exact equivalent to the oracle's standard output for any valid DNA FASTA input. You should test your script locally against the oracle to ensure convergence and exact string matching. 

Example invocation:
`python3 /home/user/analyze.py sample.fasta`